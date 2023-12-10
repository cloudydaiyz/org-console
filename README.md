![Static Badge](https://img.shields.io/badge/version-1.0-blue)
# org-console
Originating from previous membership-auto project: https://github.com/cloudydaiyz/membership-auto

This project provides a console on your local computer for updating organization files. For more information about recent updates, view the [release logs](UPDATES.md).

## How to Run
+ You can configure settings for the frontend in `frontend/config` and for the backend in `backend/config`.
+ If you've made any changes to any files in the repo (e.g. added `settings.json`), then run `docker compose build` first to rebuild the images for the frontend and backend. 
+ To run the frontend and backend, run `docker compose up` and go to `http://localhost`. 
