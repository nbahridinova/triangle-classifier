HW3a - Develop with Testing in Mind 

This assignment implements a small function that uses the GitHub REST API to list a user’s repositories and count how many commits each repository has. The main focus is  designing the code to be easy to test. All GitHub API calls are kept inside one function and the behavior is verified using unit tests that mock requests.get. Continuous Integration (Travis CI) is configured to run both the Triangle tests and the HW3a unit tests automatically on every push.
