# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2015, Numenta, Inc.  Unless you have purchased from
# Numenta, Inc. a separate commercial license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------


import json
import os
from pkg_resources import resource_stream


def GenericParams(tmImplementation):
    if (tmImplementation is "cpp"):
        paramFileRelativePath = os.path.join(
        "anomaly_params_random_encoder",
        "best_single_metric_anomaly_params_cpp.json")
    elif (tmImplementation is "tm_cpp"):
        paramFileRelativePath = os.path.join(
        "anomaly_params_random_encoder",
        "best_single_metric_anomaly_params_tm_cpp.json")
    else:
        raise ValueError("Invalid string for tmImplementation. \
                     Try cpp or tm_cpp")
    
    with resource_stream(__name__, paramFileRelativePath) as infile:
        params = json.load(infile) 
    return params