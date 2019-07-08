"""trying automatic"""

import os
import logging
from pathlib import Path

from flask import Flask, jsonify, render_template

from authomatic.extras.flask import FlaskAuthomatic
from authomatic.providers.oauth2 import GitHub

log = logging.getLogger(__name__)

here = Path(__file__).absolute().parent
template_folder = here / "build"
static_folder = template_folder / "static"
app = Flask(
    import_name=__name__,
    template_folder=str(template_folder.absolute()),
    static_folder=str(static_folder.absolute()),

)
app.secret_key = os.getenv("SECRET_KEY", "foo" * 3)

fa = FlaskAuthomatic(
    config={
        "github": {
            "class_": GitHub,
            "consumer_key": os.environ["GITHUB_KEY"],
            "consumer_secret": os.environ["GITHUB_SECRET"],
            "scope": ["repo", "user"],
            "access_headers": {"User-Agent": "huckins1"},
        }
    },
    secret=app.secret_key,
)


@app.route("/")
@fa.login("github")
def index():
    if fa.result:
        if fa.result.error:
            log.info("fa got error")
            return fa.result.error.message
        elif fa.result.user:
            log.info("fa got user %s", fa.result.user)
            if not (fa.result.user.name and fa.result.user.id):
                fa.result.user.update()
            return render_template("index.html")
        return jsonify(msg="Failure to login")
    else:
        return fa.response


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0", port=8080, debug=True)
