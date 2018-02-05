# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utility functions for interacting with a java installation."""

import re
import subprocess

from googlecloudsdk.core import exceptions
from googlecloudsdk.core.util import files


class JavaError(exceptions.Error):
  pass


def RequireJavaInstalled(for_text, min_version=7):
  """Require that a certain version of Java is installed.

  Args:
    for_text: str, the text explaining what Java is necessary for.
    min_version: int, the minimum major version to check for.

  Raises:
    JavaError: if a Java executable is not found or has the wrong version.

  Returns:
    str, Path to the Java executable.
  """
  java_path = files.FindExecutableOnPath('java')
  if not java_path:
    raise JavaError('To use the {for_text}, a Java {v}+ JRE must be installed '
                    'and on your system PATH'.format(for_text=for_text,
                                                     v=min_version))
  try:
    output = subprocess.check_output([java_path, '-version'],
                                     stderr=subprocess.STDOUT)
  except subprocess.CalledProcessError:
    raise JavaError('Unable to execute the java that was found on your PATH.'
                    ' The {for_text} requires a Java {v}+ JRE installed and on '
                    'your system PATH'.format(for_text=for_text, v=min_version))

  java_exec_version_error = JavaError(
      'The java executable on your PATH is not a Java {v}+ JRE.'
      ' The {for_text} requires a Java {v}+ JRE installed and on '
      'your system PATH'.format(v=min_version, for_text=for_text))

  match = re.search(r'version "(\d+)\.(\d+)\.', output)
  if not match:
    raise java_exec_version_error

  major_version = int(match.group(1))
  minor_version = int(match.group(2))
  # Java <= 8 used 1.X version format. Java > 8 uses X.* version format.
  if ((major_version == 1 and minor_version < min_version) or
      (major_version > 1 and major_version < min_version)):
    raise java_exec_version_error

  return java_path