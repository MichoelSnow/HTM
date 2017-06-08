modelParams = permutations_runner.runWithConfig(swarmConfig,{"maxWorkers": maxWorkers, "overwrite": True},outputLabel=outputLabel,outDir=permWorkDir,permWorkDir=permWorkDir,verbosity=0)
    def runWithConfig(swarmConfig, options,outDir=None, outputLabel="default",permWorkDir=None, verbosity=1):
        global g_currentVerbosityLevel
        g_currentVerbosityLevel = verbosity
        if outDir is None:
            outDir = os.getcwd()
        if permWorkDir is None:
            permWorkDir = os.getcwd()
        _checkOverwrite(options, outDir)
            def _checkOverwrite(options, outDir):
                overwrite = options["overwrite"]
                if not overwrite:
                    for name in ("description.py", "permutations.py"):
                        if os.path.exists(os.path.join(outDir, name)):
                            raise RuntimeError("The %s file already exists and will be ""overwritten by this tool. If it is OK to overwrite ""this file, use the --overwrite option." % os.path.join(outDir, "description.py"))
                del options["overwrite"]
        _generateExpFilesFromSwarmDescription(swarmConfig, outDir)
            def _generateExpFilesFromSwarmDescription(swarmDescriptionJson, outDir):
                # The expGenerator expects the JSON without newlines for an unknown reason.
                expDescConfig = json.dumps(swarmDescriptionJson)
                expDescConfig = expDescConfig.splitlines()
                expDescConfig = "".join(expDescConfig)
                expGenerator(["--description=%s" % (expDescConfig),"--outDir=%s" % (outDir)])
                    def expGenerator(args):
                        """ Parses, validates, and executes command-line options;     On success: Performs requested operation and exits program normally     On Error:   Dumps exception/error info in JSON format to stdout and exits the program with non-zero status. """
                        # -----------------------------------------------------------------
                        # Parse command line options
                        parser = OptionParser()
                        parser.set_usage("%prog [options] --description='{json object with args}'\n" + "%prog [options] --descriptionFromFile='{filename}'\n" + "%prog [options] --showSchema")
                        parser.add_option("--description", dest = "description", help = "Tells ExpGenerator to generate an experiment description.py and permutations.py file using the given JSON formatted experiment description string.")
                        parser.add_option("--descriptionFromFile", dest = 'descriptionFromFile', help = "Tells ExpGenerator to open the given filename and use it's contents as the JSON formatted experiment description.")
                        parser.add_option("--claDescriptionTemplateFile", dest = 'claDescriptionTemplateFile', default = 'claDescriptionTemplate.tpl', help = "The file containing the template description file for ExpGenerator [default: %default]")
                        parser.add_option("--showSchema", action="store_true", dest="showSchema", help="Prints the JSON schemas for the --description arg.")
                        parser.add_option("--version", dest = 'version', default='v2', help = "Generate the permutations file for this version of hypersearch. Possible choices are 'v1' and 'v2' [default: %default].")
                        parser.add_option("--outDir", dest = "outDir", default=None, help = "Where to generate experiment. If not specified, then a temp directory will be created")
                        (options, remainingArgs) = parser.parse_args(args)
                        # -----------------------------------------------------------------
                        # Check for unprocessed args
                        if len(remainingArgs) > 0:
                            raise _InvalidCommandArgException(_makeUsageErrorStr("Unexpected command-line args: <%s>" % (' '.join(remainingArgs),), parser.get_usage()))
                        # -----------------------------------------------------------------
                        # Check for use of mutually-exclusive options
                        activeOptions = filter(lambda x: getattr(options, x) != None, ('description', 'showSchema'))
                        if len(activeOptions) > 1:
                            raise _InvalidCommandArgException(_makeUsageErrorStr(("The specified command options are mutually-exclusive: %s") % (activeOptions,), parser.get_usage()))
                        # -----------------------------------------------------------------
                        # Process requests
                        if options.showSchema:
                            _handleShowSchemaOption()
                                def _handleShowSchemaOption():
                                  """ Displays command schema to stdout and exit program """
                                  print "\n============== BEGIN INPUT SCHEMA for --description =========>>"
                                  print(json.dumps(_getExperimentDescriptionSchema(), indent=_INDENT_STEP*2))
                                  print "\n<<============== END OF INPUT SCHEMA for --description ========"
                                  return
                        elif options.description:
                            _handleDescriptionOption(options.description, options.outDir, parser.get_usage(), hsVersion=options.version, claDescriptionTemplateFile = options.claDescriptionTemplateFile)
                                def _handleDescriptionOption(cmdArgStr, outDir, usageStr, hsVersion, claDescriptionTemplateFile):
                                    """ Parses and validates the --description option args and executes the request
                                    Parameters:
                                    -----------------------------------------------------------------------
                                    cmdArgStr:  JSON string compatible with _gExperimentDescriptionSchema
                                    outDir:     where to place generated experiment files
                                    usageStr:   program usage string
                                    hsVersion:  which version of hypersearch permutations file to generate, can be 'v1' or 'v2'
                                    claDescriptionTemplateFile: Filename containing the template description
                                    retval:     nothing """
                                    # convert --description arg from JSON string to dict
                                    try:
                                        args = json.loads(cmdArgStr)
                                    except Exception, e:
                                        raise _InvalidCommandArgException(_makeUsageErrorStr(("JSON arg parsing failed for --description: %s\n" + "ARG=<%s>") % (str(e), cmdArgStr), usageStr))
                                    #print "PARSED JSON ARGS=\n%s" % (json.dumps(args, indent=4))
                                    filesDescription = _generateExperiment(args, outDir, hsVersion=hsVersion, claDescriptionTemplateFile = claDescriptionTemplateFile)
                                        def _generateExperiment(options, outputDirPath, hsVersion, claDescriptionTemplateFile):
                                            """ Executes the --description option, which includes:
                                                1. Perform provider compatibility checks
                                                2. Preprocess the training and testing datasets (filter, join providers)
                                                3. If test dataset omitted, split the training dataset into training and testing datasets.
                                                4. Gather statistics about the training and testing datasets.
                                                5. Generate experiment scripts (description.py, permutaions.py)
                                            Parameters:
                                            --------------------------------------------------------------------------
                                            options:  dictionary that matches the schema defined by the return value of _getExperimentDescriptionSchema();  NOTE: this arg may be modified by this function.
                                            outputDirPath:  where to place generated files
                                            hsVersion:  which version of hypersearch permutations file to generate, can be 'v1' or 'v2'
                                            claDescriptionTemplateFile: Filename containing the template description
                                            Returns:    on success, returns a dictionary per _experimentResultsJSONSchema; raises exception on error
                                                Assumption1: input train and test files have identical field metadata
                                            """
                                            _gExperimentDescriptionSchema = _getExperimentDescriptionSchema()
                                            # Validate JSON arg using JSON schema validator
                                            try:
                                                validictory.validate(options, _gExperimentDescriptionSchema)
                                            except Exception, e:
                                                raise _InvalidCommandArgException(("JSON arg validation failed for option --description: " + "%s\nOPTION ARG=%s") % (str(e), pprint.pformat(options)))
                                            # Validate the streamDef
                                            streamSchema = json.load(resource_stream(jsonschema.__name__,'stream_def.json'))
                                            try:
                                                validictory.validate(options['streamDef'], streamSchema)
                                            except Exception, e:
                                                raise _InvalidCommandArgException(("JSON arg validation failed for streamDef " + "%s\nOPTION ARG=%s") % (str(e), json.dumps(options)))
                                            # -----------------------------------------------------------------------
                                            # Handle legacy parameters from JAVA API server
                                            # TODO: remove this!
                                            _handleJAVAParameters(options)
                                            # -----------------------------------------------------------------------
                                            # Get default values
                                            for propertyName in _gExperimentDescriptionSchema['properties']:
                                                _getPropertyValue(_gExperimentDescriptionSchema, propertyName, options)
                                            if options['inferenceArgs'] is not None:
                                                infArgs = _gExperimentDescriptionSchema['properties']['inferenceArgs']
                                                for schema in infArgs['type']:
                                                    if isinstance(schema, dict):
                                                        for propertyName in schema['properties']:
                                                            _getPropertyValue(schema, propertyName, options['inferenceArgs'])
                                            if options['anomalyParams'] is not None:
                                                anomalyArgs = _gExperimentDescriptionSchema['properties']['anomalyParams']
                                                for schema in anomalyArgs['type']:
                                                    if isinstance(schema, dict):
                                                        for propertyName in schema['properties']:
                                                            _getPropertyValue(schema, propertyName, options['anomalyParams'])
                                            # If the user specified nonTemporalClassification, make sure prediction steps is 0
                                            predictionSteps = options['inferenceArgs'].get('predictionSteps', None)
                                            if options['inferenceType'] == InferenceType.NontemporalClassification:
                                                if predictionSteps is not None and predictionSteps != [0]:
                                                    raise RuntimeError("When NontemporalClassification is used, prediction steps must be [0]")
                                            # -------------------------------------------------------------------------
                                            # If the user asked for 0 steps of prediction, then make this a spatial
                                            #  classification experiment
                                            if predictionSteps == [0] and options['inferenceType'] in ['NontemporalMultiStep', 'TemporalMultiStep', 'MultiStep']:
                                                options['inferenceType'] = InferenceType.NontemporalClassification
                                            # If NontemporalClassification was chosen as the inferenceType, then the
                                            #  predicted field can NOT be used as an input
                                            if options["inferenceType"] == InferenceType.NontemporalClassification:
                                                if options["inferenceArgs"]["inputPredictedField"] == "yes" or options["inferenceArgs"]["inputPredictedField"] == "auto":
                                                    raise RuntimeError("When the inference type is NontemporalClassification inputPredictedField must be set to 'no'")
                                                options["inferenceArgs"]["inputPredictedField"] = "no"
                                            # -----------------------------------------------------------------------
                                            # Process the swarmSize setting, if provided
                                            swarmSize = options['swarmSize']
                                            if swarmSize is None:
                                                if options["inferenceArgs"]["inputPredictedField"] is None:
                                                    options["inferenceArgs"]["inputPredictedField"] = "auto"
                                            elif swarmSize == 'small':
                                                if options['minParticlesPerSwarm'] is None:
                                                    options['minParticlesPerSwarm'] = 3
                                                if options['iterationCount'] is None:
                                                    options['iterationCount'] = 100
                                                if options['maxModels'] is None:
                                                    options['maxModels'] = 1
                                                if options["inferenceArgs"]["inputPredictedField"] is None:
                                                    options["inferenceArgs"]["inputPredictedField"] = "yes"
                                            elif swarmSize == 'medium':
                                                if options['minParticlesPerSwarm'] is None:
                                                    options['minParticlesPerSwarm'] = 5
                                                if options['iterationCount'] is None:
                                                    options['iterationCount'] = 4000
                                                if options['maxModels'] is None:
                                                    options['maxModels'] = 200
                                                if options["inferenceArgs"]["inputPredictedField"] is None:
                                                    options["inferenceArgs"]["inputPredictedField"] = "auto"
                                            elif swarmSize == 'large':
                                                if options['minParticlesPerSwarm'] is None:
                                                    options['minParticlesPerSwarm'] = 15
                                                    #options['killUselessSwarms'] = False
                                                    #options['minFieldContribution'] = -1000
                                                    #options['maxFieldBranching'] = 10
                                                    #options['tryAll3FieldCombinations'] = True
                                                options['tryAll3FieldCombinationsWTimestamps'] = True
                                                if options["inferenceArgs"]["inputPredictedField"] is None:
                                                    options["inferenceArgs"]["inputPredictedField"] = "auto"
                                            else:
                                                raise RuntimeError("Unsupported swarm size: %s" % (swarmSize))
                                            # -----------------------------------------------------------------------
                                            # Get token replacements
                                            tokenReplacements = dict()
                                            #--------------------------------------------------------------------------
                                            # Generate the encoder related substitution strings
                                            includedFields = options['includedFields']
                                            if hsVersion == 'v1':
                                                (encoderSpecsStr, permEncoderChoicesStr) = _generateEncoderStringsV1(includedFields)
                                            elif hsVersion in ['v2', 'ensemble']:
                                                (encoderSpecsStr, permEncoderChoicesStr) = _generateEncoderStringsV2(includedFields, options)
                                            else:
                                                raise RuntimeError("Unsupported hsVersion of %s" % (hsVersion))
                                            #--------------------------------------------------------------------------
                                            # Generate the string containing the sensor auto-reset dict.
                                            if options['resetPeriod'] is not None:
                                                sensorAutoResetStr = pprint.pformat(options['resetPeriod'],indent=2*_INDENT_STEP)
                                            else:
                                                sensorAutoResetStr = 'None'
                                            #--------------------------------------------------------------------------
                                            # Generate the string containing the aggregation settings.
                                            aggregationPeriod = {'days': 0,'hours': 0,'microseconds': 0,'milliseconds': 0,'minutes': 0,'months': 0,'seconds': 0,'weeks': 0,'years': 0,}
                                            # Honor any overrides provided in the stream definition
                                            aggFunctionsDict = {}
                                            if 'aggregation' in options['streamDef']:
                                                for key in aggregationPeriod.keys():
                                                    if key in options['streamDef']['aggregation']:
                                                        aggregationPeriod[key] = options['streamDef']['aggregation'][key]
                                                if 'fields' in options['streamDef']['aggregation']:
                                                    for (fieldName, func) in options['streamDef']['aggregation']['fields']:
                                                        aggFunctionsDict[fieldName] = str(func)
                                            # Do we have any aggregation at all?
                                            hasAggregation = False
                                            for v in aggregationPeriod.values():
                                                if v != 0:
                                                    hasAggregation = True
                                                    break
                                            # Convert the aggFunctionsDict to a list
                                            aggFunctionList = aggFunctionsDict.items()
                                            aggregationInfo = dict(aggregationPeriod)
                                            aggregationInfo['fields'] = aggFunctionList
                                            # Form the aggregation strings
                                            aggregationInfoStr = "%s" % (pprint.pformat(aggregationInfo,indent=2*_INDENT_STEP))
                                            # -----------------------------------------------------------------------
                                            # Generate the string defining the dataset. This is basically the
                                            #  streamDef, but referencing the aggregation we already pulled out into the
                                            #  config dict (which enables permuting over it)
                                            datasetSpec = options['streamDef']
                                            if 'aggregation' in datasetSpec:
                                                datasetSpec.pop('aggregation')
                                            if hasAggregation:
                                                datasetSpec['aggregation'] = '$SUBSTITUTE'
                                            datasetSpecStr = pprint.pformat(datasetSpec, indent=2*_INDENT_STEP)
                                            datasetSpecStr = datasetSpecStr.replace("'$SUBSTITUTE'", "config['aggregationInfo']")
                                            datasetSpecStr = _indentLines(datasetSpecStr, 2, indentFirstLine=False)
                                            # -----------------------------------------------------------------------
                                            # Was computeInterval specified with Multistep prediction? If so, this swarm should permute over different aggregations
                                            computeInterval = options['computeInterval']
                                            if computeInterval is not None and options['inferenceType'] in ['NontemporalMultiStep','TemporalMultiStep','MultiStep']:
                                                # Compute the predictAheadTime based on the minAggregation (specified in the stream definition) and the number of prediction steps
                                                predictionSteps = options['inferenceArgs'].get('predictionSteps', [1])
                                                if len(predictionSteps) > 1:
                                                    raise _InvalidCommandArgException("Invalid predictionSteps: %s. When computeInterval is specified, there can only be one stepSize in predictionSteps." % predictionSteps)
                                                if max(aggregationInfo.values()) == 0:
                                                    raise _InvalidCommandArgException("Missing or nil stream aggregation: When computeInterval is specified, then the stream aggregation interval must be non-zero.")
                                                # Compute the predictAheadTime
                                                numSteps = predictionSteps[0]
                                                predictAheadTime = dict(aggregationPeriod)
                                                for key in predictAheadTime.iterkeys():
                                                    predictAheadTime[key] *= numSteps
                                                predictAheadTimeStr = pprint.pformat(predictAheadTime,indent=2*_INDENT_STEP)
                                                # This tells us to plug in a wildcard string for the prediction steps that we use in other parts of the description file (metrics, inferenceArgs, etc.)
                                                options['dynamicPredictionSteps'] = True
                                            else:
                                                options['dynamicPredictionSteps'] = False
                                                predictAheadTimeStr = "None"
                                            # -----------------------------------------------------------------------
                                            # Save environment-common token substitutions
                                            tokenReplacements['\$EXP_GENERATOR_PROGRAM_PATH'] = _quoteAndEscape(os.path.abspath(__file__))
                                            # If the "uber" metric 'MultiStep' was specified, then plug in TemporalMultiStep by default
                                            inferenceType = options['inferenceType']
                                            if inferenceType == 'MultiStep':
                                                inferenceType = InferenceType.TemporalMultiStep
                                            tokenReplacements['\$INFERENCE_TYPE'] = "'%s'" % inferenceType
                                            # Nontemporal classificaion uses only encoder and classifier
                                            if inferenceType == InferenceType.NontemporalClassification:
                                                tokenReplacements['\$SP_ENABLE'] = "False"
                                                tokenReplacements['\$TP_ENABLE'] = "False"
                                            else:
                                                tokenReplacements['\$SP_ENABLE'] = "True"
                                                tokenReplacements['\$TP_ENABLE'] = "True"
                                                tokenReplacements['\$CLA_CLASSIFIER_IMPL'] = ""
                                            tokenReplacements['\$ANOMALY_PARAMS'] = pprint.pformat(options['anomalyParams'], indent=2*_INDENT_STEP)
                                            tokenReplacements['\$ENCODER_SPECS'] = encoderSpecsStr
                                            tokenReplacements['\$SENSOR_AUTO_RESET'] = sensorAutoResetStr
                                            tokenReplacements['\$AGGREGATION_INFO'] = aggregationInfoStr
                                            tokenReplacements['\$DATASET_SPEC'] = datasetSpecStr
                                            if options['iterationCount'] is None:
                                                options['iterationCount'] = -1
                                            tokenReplacements['\$ITERATION_COUNT'] = str(options['iterationCount'])
                                            tokenReplacements['\$SP_POOL_PCT'] = str(options['spCoincInputPoolPct'])
                                            tokenReplacements['\$HS_MIN_PARTICLES'] = str(options['minParticlesPerSwarm'])
                                            tokenReplacements['\$SP_PERM_CONNECTED'] = str(options['spSynPermConnected'])
                                            tokenReplacements['\$FIELD_PERMUTATION_LIMIT'] = str(options['fieldPermutationLimit'])
                                            tokenReplacements['\$PERM_ENCODER_CHOICES'] = permEncoderChoicesStr
                                            predictionSteps = options['inferenceArgs'].get('predictionSteps', [1])
                                            predictionStepsStr = ','.join([str(x) for x in predictionSteps])
                                            tokenReplacements['\$PREDICTION_STEPS'] = "'%s'" % (predictionStepsStr)
                                            tokenReplacements['\$PREDICT_AHEAD_TIME'] = predictAheadTimeStr
                                            # Option permuting over SP synapse decrement value
                                            tokenReplacements['\$PERM_SP_CHOICES'] = ""
                                            if options['spPermuteDecrement'] and options['inferenceType'] != 'NontemporalClassification': 
                                                tokenReplacements['\$PERM_SP_CHOICES'] = _ONE_INDENT +"'synPermInactiveDec': PermuteFloat(0.0003, 0.1),\n"
                                            # The TP permutation parameters are not required for non-temporal networks
                                            if options['inferenceType'] in ['NontemporalMultiStep','NontemporalClassification']:
                                                tokenReplacements['\$PERM_TP_CHOICES'] = ""
                                            else:
                                                tokenReplacements['\$PERM_TP_CHOICES'] = "  'activationThreshold': PermuteInt(12, 16),\n" + "  'minThreshold': PermuteInt(9, 12),\n" + "  'pamLength': PermuteInt(1, 5),\n"
                                            # If the inference type is just the generic 'MultiStep', then permute over temporal/nonTemporal multistep
                                            if options['inferenceType'] == 'MultiStep':
                                                tokenReplacements['\$PERM_INFERENCE_TYPE_CHOICES'] = "  'inferenceType': PermuteChoices(['NontemporalMultiStep', " + "'TemporalMultiStep']),"
                                            else:
                                                tokenReplacements['\$PERM_INFERENCE_TYPE_CHOICES'] = ""
                                          # The Classifier permutation parameters are only required for Multi-step inference types
                                            if options['inferenceType'] in ['NontemporalMultiStep', 'TemporalMultiStep','MultiStep', 'TemporalAnomaly', 'NontemporalClassification']:
                                                tokenReplacements['\$PERM_CL_CHOICES'] = "  'alpha': PermuteFloat(0.0001, 0.1),\n"
                                            else:
                                                tokenReplacements['\$PERM_CL_CHOICES'] = ""
                                            # The Permutations alwaysIncludePredictedField setting. * When the experiment description has 'inputPredictedField' set to 'no', we  simply do not put in an encoder for the predicted field.  * When 'inputPredictedField' is set to 'auto', we include an encoder for the #   predicted field and swarming tries it out just like all the other fields. * When 'inputPredictedField' is set to 'yes', we include this setting in  the permutations file which informs swarming to always use the  predicted field (the first swarm will be the predicted field only) 
                                            tokenReplacements['\$PERM_ALWAYS_INCLUDE_PREDICTED_FIELD'] = "inputPredictedField = '%s'" % (options["inferenceArgs"]["inputPredictedField"])  
                                            # The Permutations minFieldContribution setting
                                            if options.get('minFieldContribution', None) is not None:
                                                tokenReplacements['\$PERM_MIN_FIELD_CONTRIBUTION'] = "minFieldContribution = %d" % (options['minFieldContribution']) 
                                            else:
                                                tokenReplacements['\$PERM_MIN_FIELD_CONTRIBUTION'] = ""
                                          # The Permutations killUselessSwarms setting
                                          if options.get('killUselessSwarms', None) is not None:
                                            tokenReplacements['\$PERM_KILL_USELESS_SWARMS'] = \
                                                "killUselessSwarms = %r" % (options['killUselessSwarms']) 
                                          else:
                                            tokenReplacements['\$PERM_KILL_USELESS_SWARMS'] = ""

                                          # The Permutations maxFieldBranching setting
                                          if options.get('maxFieldBranching', None) is not None:
                                            tokenReplacements['\$PERM_MAX_FIELD_BRANCHING'] = \
                                                "maxFieldBranching = %r" % (options['maxFieldBranching']) 
                                          else:
                                            tokenReplacements['\$PERM_MAX_FIELD_BRANCHING'] = ""

                                          # The Permutations tryAll3FieldCombinations setting
                                          if options.get('tryAll3FieldCombinations', None) is not None:
                                            tokenReplacements['\$PERM_TRY_ALL_3_FIELD_COMBINATIONS'] = \
                                                "tryAll3FieldCombinations = %r" % (options['tryAll3FieldCombinations']) 
                                          else:
                                            tokenReplacements['\$PERM_TRY_ALL_3_FIELD_COMBINATIONS'] = ""

                                          # The Permutations tryAll3FieldCombinationsWTimestamps setting
                                          if options.get('tryAll3FieldCombinationsWTimestamps', None) is not None:
                                            tokenReplacements['\$PERM_TRY_ALL_3_FIELD_COMBINATIONS_W_TIMESTAMPS'] = \
                                                "tryAll3FieldCombinationsWTimestamps = %r" % \
                                                        (options['tryAll3FieldCombinationsWTimestamps']) 
                                          else:
                                            tokenReplacements['\$PERM_TRY_ALL_3_FIELD_COMBINATIONS_W_TIMESTAMPS'] = ""


                                          # The Permutations fieldFields setting
                                          if options.get('fixedFields', None) is not None:
                                            tokenReplacements['\$PERM_FIXED_FIELDS'] = \
                                                "fixedFields = %r" % (options['fixedFields']) 
                                          else:
                                            tokenReplacements['\$PERM_FIXED_FIELDS'] = ""

                                          # The Permutations fastSwarmModelParams setting
                                          if options.get('fastSwarmModelParams', None) is not None:
                                            tokenReplacements['\$PERM_FAST_SWARM_MODEL_PARAMS'] = \
                                                "fastSwarmModelParams = %r" % (options['fastSwarmModelParams']) 
                                          else:
                                            tokenReplacements['\$PERM_FAST_SWARM_MODEL_PARAMS'] = ""


                                          # The Permutations maxModels setting
                                          if options.get('maxModels', None) is not None:
                                            tokenReplacements['\$PERM_MAX_MODELS'] = \
                                                "maxModels = %r" % (options['maxModels']) 
                                          else:
                                            tokenReplacements['\$PERM_MAX_MODELS'] = ""


                                          # --------------------------------------------------------------------------
                                          # The Aggregation choices have to be determined when we are permuting over
                                          #   aggregations.
                                          if options['dynamicPredictionSteps']:
                                            debugAgg = True

                                            # First, we need to error check to insure that computeInterval is an integer
                                            #  multiple of minAggregation (aggregationPeriod)
                                            quotient = aggregationDivide(computeInterval, aggregationPeriod)
                                            (isInt, multiple) = _isInt(quotient)
                                            if not isInt or multiple < 1:
                                              raise _InvalidCommandArgException("Invalid computeInterval: %s. "
                                                      "computeInterval must be an integer multiple of the stream "
                                                      "aggregation (%s)." % (computeInterval, aggregationPeriod))


                                            # The valid aggregation choices are governed by the following constraint,
                                            #   1.) (minAggregation * N) * M = predictAheadTime
                                            #       (minAggregation * N) * M = maxPredictionSteps * minAggregation
                                            #       N * M = maxPredictionSteps
                                            #
                                            #   2.) computeInterval = K * aggregation
                                            #       computeInterval = K * (minAggregation * N)
                                            #
                                            # where: aggregation = minAggregation * N
                                            #        K, M and N are integers >= 1
                                            #          N = aggregation / minAggregation
                                            #          M = predictionSteps, for a particular aggregation
                                            #          K = number of predictions within each compute interval
                                            #

                                            # Let's build up a a list of the possible N's that satisfy the
                                            #  N * M = maxPredictionSteps constraint
                                            mTimesN = float(predictionSteps[0])
                                            possibleNs = []
                                            for n in xrange(1, int(mTimesN)+1):
                                              m = mTimesN / n
                                              mInt = int(round(m))
                                              if mInt < 1:
                                                break
                                              if abs(m - mInt) > 0.0001 * m:
                                                continue
                                              possibleNs.append(n)

                                            if debugAgg:
                                              print "All integer factors of %d are: %s" % (mTimesN, possibleNs)

                                            # Now go through and throw out any N's that don't satisfy the constraint:
                                            #  computeInterval = K * (minAggregation * N)
                                            aggChoices = []
                                            for n in possibleNs:
                                              # Compute minAggregation * N
                                              agg = dict(aggregationPeriod)
                                              for key in agg.iterkeys():
                                                agg[key] *= n

                                              # Make sure computeInterval is an integer multiple of the aggregation
                                              # period
                                              quotient = aggregationDivide(computeInterval, agg)
                                              #print computeInterval, agg
                                              #print quotient
                                              #import sys; sys.exit()
                                              (isInt, multiple) = _isInt(quotient)
                                              if not isInt or multiple < 1:
                                                continue
                                              aggChoices.append(agg)

                                            # Only eveluate up to 5 different aggregations
                                            aggChoices = aggChoices[-5:]

                                            if debugAgg:
                                              print "Aggregation choices that will be evaluted during swarming:"
                                              for agg in aggChoices:
                                                print "  ==>", agg
                                              print

                                            tokenReplacements['\$PERM_AGGREGATION_CHOICES'] = (
                                                "PermuteChoices(%s)" % (
                                                    pprint.pformat(aggChoices, indent=2*_INDENT_STEP)))

                                          else:
                                            tokenReplacements['\$PERM_AGGREGATION_CHOICES'] = aggregationInfoStr



                                          # Generate the inferenceArgs replacement tokens
                                          _generateInferenceArgs(options, tokenReplacements)

                                          # Generate the metric replacement tokens
                                          _generateMetricsSubstitutions(options, tokenReplacements)


                                          # -----------------------------------------------------------------------
                                          # Generate Control dictionary
                                          environment = options['environment']
                                          if environment == OpfEnvironment.Nupic:
                                            tokenReplacements['\$ENVIRONMENT'] = "'%s'"%OpfEnvironment.Nupic
                                            controlTemplate = "nupicEnvironmentTemplate.tpl"
                                          elif environment == OpfEnvironment.Experiment:
                                            tokenReplacements['\$ENVIRONMENT'] = "'%s'"%OpfEnvironment.Experiment
                                            controlTemplate = "opfExperimentTemplate.tpl"
                                          else:
                                            raise _InvalidCommandArgException("Invalid environment type %s"% environment)

                                          # -----------------------------------------------------------------------
                                          if outputDirPath is None:
                                            outputDirPath = tempfile.mkdtemp()
                                          if not os.path.exists(outputDirPath):
                                            os.makedirs(outputDirPath)

                                          print "Generating experiment files in directory: %s..." % (outputDirPath)
                                          descriptionPyPath = os.path.join(outputDirPath, "description.py")
                                          _generateFileFromTemplates([claDescriptionTemplateFile, controlTemplate],
                                                                      descriptionPyPath,
                                                                      tokenReplacements)

                                          permutationsPyPath = os.path.join(outputDirPath, "permutations.py")

                                          if hsVersion == 'v1':
                                            _generateFileFromTemplates(['permutationsTemplateV1.tpl'],permutationsPyPath,
                                                                    tokenReplacements)
                                          elif hsVersion == 'ensemble':
                                            _generateFileFromTemplates(['permutationsTemplateEnsemble.tpl'],permutationsPyPath,
                                                                    tokenReplacements)
                                          elif hsVersion == 'v2':
                                            _generateFileFromTemplates(['permutationsTemplateV2.tpl'],permutationsPyPath,
                                                                    tokenReplacements)
                                          else:
                                            raise(ValueError("This permutation version is not supported yet: %s" %
                                                                hsVersion))

                                          print "done."
  
  
  
                                    pprint.pprint(filesDescription)
                                    return
                        elif options.descriptionFromFile:
                            _handleDescriptionFromFileOption(options.descriptionFromFile, options.outDir, parser.get_usage(), hsVersion=options.version, claDescriptionTemplateFile = options.claDescriptionTemplateFile)
                        else:
                            raise _InvalidCommandArgException(_makeUsageErrorStr("Error in validating command options. No option provided:\n", parser.get_usage()))
        options["expDescConfig"] = swarmConfig
        options["outputLabel"] = outputLabel
        options["outDir"] = outDir
        options["permWorkDir"] = permWorkDir
        runOptions = _injectDefaultOptions(options)
        _validateOptions(runOptions)
        return _runAction(runOptions)
            def _runAction(runOptions):
                if not os.path.exists(runOptions["outDir"]):
                    os.makedirs(runOptions["outDir"])
                if not os.path.exists(runOptions["permWorkDir"]):
                    os.makedirs(runOptions["permWorkDir"])
                action = runOptions["action"]
                # Print Nupic HyperSearch results from the current or last run
                if action == "report":
                    returnValue = _HyperSearchRunner.generateReport(options=runOptions, replaceReport=runOptions["replaceReport"], hyperSearchJob=None, metricsKeys=None)
                # Run HyperSearch
                elif action in ("run", "dryRun", "pickup"):
                    returnValue = _runHyperSearch(runOptions)
                        def _runHyperSearch(runOptions):
                            global gCurrentSearch
                            # Run HyperSearch
                            startTime = time.time()
                            search = _HyperSearchRunner(runOptions)
                            # Save in global for the signal handler.
                            gCurrentSearch = search
                            if runOptions["action"] in ("run", "dryRun"):
                                search.runNewSearch()
                            else:
                                search.pickupSearch()
                            # Generate reports
                            # Print results and generate report csv file
                            modelParams = _HyperSearchRunner.generateReport(options=runOptions, replaceReport=runOptions["replaceReport"], hyperSearchJob=search.peekSearchJob(), metricsKeys=search.getDiscoveredMetricsKeys())
                            secs = time.time() - startTime
                            hours = int(secs) / (60 * 60)
                            secs -= hours * (60 * 60)
                            minutes = int(secs) / 60
                            secs -= minutes * 60
                            print "Elapsed time (h:mm:ss): %d:%02d:%02d" % (hours, minutes, int(secs))
                            jobID = search.peekSearchJob().getJobID()
                            print "Hypersearch ClientJobs job ID: ", jobID
                    else:
                    raise Exception("Unhandled action: %s" % action)
                return returnValue


 
 
modelParamsFile = writeModelParamsToFile(modelParams, name)





    _handleDescriptionOption
        _generateExperiment
            _generateEncoderStringsV2 - XX
                _generatePermEncoderStr - XX