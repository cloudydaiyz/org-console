![Static Badge](https://img.shields.io/badge/version-1.0-blue)
# org-console
Originating from previous membership-auto project: https://github.com/cloudydaiyz/membership-auto

This project provides a console on your local computer for updating organization files. For more information about recent updates, view the [release logs](UPDATES.md).

4/24/24: This project is now considered legacy -- it won't be updated anymore. Check out [the membership-logger project](https://github.com/cloudydaiyz/membership-logger) for a more up-to-date version!

## How to Run
+ You can configure settings for the frontend in `frontend/config` and for the backend in `backend/config`.
+ If you've made any changes to any files in the repo (e.g. added `settings.json`), then run `docker compose build` first to rebuild the images for the frontend and backend. 
+ To run the frontend and backend, run `docker compose up` and go to `http://localhost`. 
