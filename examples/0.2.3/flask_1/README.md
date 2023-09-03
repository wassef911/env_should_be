# Flask example

in this example env_should_be is included in the requirements.txt, and we are starting two containers from the same image...

external-app will call admins if it was ever started in an environment that doesn't match the description... (in this case 2 descriptions)

internal-app will be allowed to to proceed in the entrypoint script even with a failing environment...
this is usefull for less-important-deployments/experiments/debug...

```sh
#### EXTERNAL APP
external-app_1  |  * Debug mode: off
external-app_1  |  * Running on all addresses (0.0.0.0)
external-app_1  |  * Running on http://127.0.0.1:5000
external-app_1  |  * Running on http://172.28.0.2:5000
#### INTERNAL APP
internal-app_1  | WARNING: Env Not matching /app/description/db.json
internal-app_1  | ERROR:
internal-app_1  |  DB_PASSWORD, failing to match ['length']
internal-app_1  |  * Debug mode: off
internal-app_1  |  * Running on all addresses (0.0.0.0)
internal-app_1  |  * Running on http://127.0.0.1:5000
internal-app_1  |  * Running on http://172.28.0.3:5000
```
