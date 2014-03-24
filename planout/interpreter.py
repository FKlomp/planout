# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from copy import deepcopy
from ops.utils import Operators
from mapper import Mapper


Operators.initFactory()

class InterpreterMapper(Mapper):
  """PlanOut interpreter"""

  def __init__(self, serialization, experiment_salt='global_salt', inputs={}):
    self._serialization = serialization
    self._env = {}
    self._overrides = {}
    self._experiment_salt = experiment_salt
    self._evaluated = False
    self._inputs = deepcopy(inputs)

  def get_params(self):
    if not self._evaluated:
      self.evaluate(self._serialization)
      self._evaluated = True
    return self._env

  def set_env(self, new_env):
    self._env = deepcopy(new_env)
    for v in self._overrides:
      self._env[v] = self._overrides[v]
    return self

  def has(self, name):
    return name in self._env

  def get(self, name, default=None):
    return self._env.get(name, self._inputs.get(name, default))

  def set(self, name, value):
    self._env[name] = value
    return self

  def set_overrides(self, overrides):
    Operators.enable_overrides()
    self._overrides = overrides
    self.set_env(self._env)  # this will reset overrides
    return self

  def has_override(self, name):
    return name in self._overrides

  def get_overrides(self):
    return self._overrides

  def evaluate(self, data):
    if Operators.isOperator(data):
      return Operators.operatorInstance(data).execute(self)
    elif type(data) is list:
      return [self.evaluate(i) for i in data]
    else:
      return data  # data is a literal


class InterpreterInspector():
  """Class for inspecting serialized PlanOut experiment definitions"""
  def __init__(self, serialization):
    self._serialization = serialization

  def validate(self):
    """validate PlanOut serialization"""
    config = self._serialization
    return Operators.validateOperator(config)

  def pretty(self):
    """pretty print PlanOut serialization as PlanOut language code"""
    config = self._serialization
    return Operators.operatorInstance(config).pretty()

  def get_variables(self):
    """get all variables set by PlanOut script"""
    pass

  def get_input_variables(self):
    """get all variables used not defined by the PlanOut script"""
    pass
