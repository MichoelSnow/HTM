model = createModel(InputName)
    def createModel(InputName):
        """
        Given a model params dictionary, create a CLA Model. Automatically enables
        inference for predicted field.
        :param modelParams: Model params dict
        :return: OPF Model object
        """
        CsvCol,CsvDataTypes,CsvData,csvMin,csvMax,csvStd = getNewParams(InputName)
            def getNewParams(InputName):
                """
                
                """
                INPUT_FILE = "%s.csv" % (InputName)
                CsvData = pd.read_csv(INPUT_FILE)
                CsvCol = CsvData.columns
                CsvDataTypes = CsvData.loc[0].tolist()
                CsvData = CsvData[:][2:]
                csvMax,csvMin,csvStd = [],[],[]
                for Col,ColType in enumerate(CsvDataTypes):
                    if ColType == 'float':
                        CsvData[CsvCol[Col]] = pd.to_numeric(CsvData[CsvCol[Col]])
                        csvMax.append(CsvData[CsvCol[Col]].max())
                        csvMin.append(CsvData[CsvCol[Col]].min())
                        csvStd.append(np.std(CsvData[CsvCol[Col]]))
                    else:
                        csvMax.append(None)
                        csvMin.append(None)
                        csvStd.append(None)
                return [CsvCol,CsvDataTypes,CsvData,csvMin,csvMax,csvStd]
        # Try to find already existing params file
        try:
            params = getModelParamsFromName(InputName)
                def getModelParamsFromName(InputName):
                    """
                    Given a gym name, assumes a matching model params python module exists within the model_params directory and attempts to import it.
                    :param gymName: Gym name, used to guess the model params module name.
                    :return: OPF Model params dictionary
                    """
                    importName = "model_params.%s_model_params" % (InputName.replace(" ", "_").replace("-", "_"))
                    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
                    params = {'modelConfig': importedModelParams}
                    return params
            params["inferenceArgs"] = {'inputPredictedField':'auto','predictionSteps': [1],'predictedField': CsvCol[1]}
        except:    
            print 'swarm file not found, using generic values'
        # Get the new parameters from the csv file
            minResolution = 0.001
            tmImplementation = "cpp"
            # Load model parameters and update encoder params
            if (tmImplementation is "cpp"):
                paramFileRelativePath = os.path.join("anomaly_params_random_encoder","best_single_metric_anomaly_params_cpp.json")
            elif (tmImplementation is "tm_cpp"):
                paramFileRelativePath = os.path.join("anomaly_params_random_encoder","best_single_metric_anomaly_params_tm_cpp.json")
            else:
                raise ValueError("Invalid string for tmImplementation. Try cpp or tm_cpp")        
            with resource_stream(__name__, paramFileRelativePath) as infile:
                params = json.load(infile)
            _fixupRandomEncoderParams(params, CsvCol, CsvDataTypes, CsvData,csvMin, csvMax, csvStd, minResolution)
                def _fixupRandomEncoderParams(params, CsvCol, CsvDataTypes, CsvData, csvMin,csvMax ,csvStd, minResolution):
                    """
                    Given model params, figure out the correct parameters for the
                    RandomDistributed encoder. Modifies params in place.
                    """
                    encDict = (params["modelConfig"]["modelParams"]["sensorParams"]["encoders"])
                    numBuckets = 130.0
                    for Col,ColType in enumerate(CsvDataTypes):
                        if ColType == 'datetime':
                            Nm1 = '%s_timeOfDay' % (CsvCol[Col])
                            encDict[Nm1] = {}
                            encDict[Nm1]['type'] = 'DateEncoder'
                            encDict[Nm1]['timeOfDay'] = [21,9.49]
                            encDict[Nm1]['fieldname'] = CsvCol[Col]
                            encDict[Nm1]['name'] = CsvCol[Col]
                            Nm2 = '%s_dayOfWeek' % (CsvCol[Col])
                            encDict[Nm2] = None
                            Nm3 = '%s_weekend' % (CsvCol[Col])
                            encDict[Nm3] = None
                        elif ColType == 'float':
                            encDict[CsvCol[Col]] = {}
                            encDict[CsvCol[Col]]['name'] = CsvCol[Col]
                            encDict[CsvCol[Col]]['fieldname'] = CsvCol[Col]
                            encDict[CsvCol[Col]]['seed'] = 42
                            encDict[CsvCol[Col]]["type"] =  "RandomDistributedScalarEncoder"
                            maxVal = csvMax[Col]
                            minVal = csvMin[Col]
                            # Handle the corner case where the incoming min and max are the same
                            if minVal == maxVal:
                                maxVal = minVal + 1
                            maxVal = maxVal
                            minVal = minVal
                            resolution = max(minResolution,(maxVal - minVal) / numBuckets)
                            encDict[CsvCol[Col]]["resolution"] = resolution
        params["inferenceArgs"]["predictedField"] = CsvCol[1]
        params['modelConfig']['modelParams']['clEnable'] = True
        model = ModelFactory.create(modelConfig=params["modelConfig"])
            def create(modelConfig, logLevel=logging.ERROR):
                """ Create a new model instance, given a description dictionary.
                @param modelConfig (dict) A dictionary describing the current model `described here <../../quick-start/example-model-params.html>`_
                @param logLevel (int) The level of logging output that should be generated
                @exception (Exception) Unsupported model type
                @returns: :class:`nupic.frameworks.opf.model.Model`"""
                logger = ModelFactory.__getLogger()
                logger.setLevel(logLevel)
                logger.debug("ModelFactory returning Model from dict: %s", modelConfig)
                modelClass = None
                if modelConfig['model'] == "HTMPrediction":
                    modelClass = HTMPredictionModel
                elif modelConfig['model'] == "TwoGram":
                    modelClass = TwoGramModel
                elif modelConfig['model'] == "PreviousValue":
                    modelClass = PreviousValueModel
                else:
                    raise Exception("ModelFactory received unsupported Model type: %s" % modelConfig['model'])
                return modelClass(**modelConfig['modelParams'])
        model.enableLearning()  
        model.enableInference(params["inferenceArgs"])
        return model
runIoThroughNupic(inputData, model, InputName)
