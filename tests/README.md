# Tests

Make sure you source the virutal environment in all cases to run
tests in this way (if you are using a colcon environment, the
same commands will eventually hold once ros2's rosdep becomes
functional).

## Executing Tests

Always run tests from the root directory, since that is where
it will pick up the nosetests configuration in `setup.cfg`.

```
# All Tests via SetupTools (indirectly)
$ python setup.py nosetests
# All Tests via Nosetest (directly)
$ nosetests ./tests
# A single test
$ nosetests tests/test_oneshot.py
```

If not in the virtualenv and in a dual python environment, e.g. Ubuntu bionic,
replace those commands with their `python3 / nosetests3` equivalents.