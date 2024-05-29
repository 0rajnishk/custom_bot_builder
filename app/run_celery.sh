#!/bin/bash
# celery -A app.celery_app worker --loglevel=info

#!/bin/bash
export CELERYD_FORCE_EXECV=True
celery -A app.celery_app worker --loglevel=info --pool=solo
