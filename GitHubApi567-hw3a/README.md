[![Build Status](https://app.travis-ci.com/nbahridinova/triangle-classifier.svg?branch=main)](https://app.travis-ci.com/github/nbahridinova/triangle-classifier)

HW3a - Develop with Testing in Mind 

This assignment implements a small function that uses the GitHub REST API to list a user’s repositories and count how many commits each repository has. The main focus is  designing the code to be easy to test. All GitHub API calls are kept inside one function and the behavior is verified using unit tests that mock requests.get. Continuous Integration (Travis CI) is configured to run both the Triangle tests and the HW3a unit tests automatically on every push.

While writing the code, I focused on making it easy to test and easy to validate from the outside. I mainly focused on: 
- Mock external calls instead of hitting GitHub: Unit tests replace requests.get with mocks. This makes tests fast, consistent, and not dependent on network or GitHub being available.
- Test both success and failure cases.
- CI automation: Travis CI runs the Triangle tests and the HW3a tests automatically, so I can confirm everything still works after each change.
The main challenge is that GitHub enforces rate limits, so tests that call the real API can fail even if the code is correct.
