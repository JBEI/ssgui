# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.run import Run # noqa
from app.models.sample import Sample # noqa
from app.models.template import Template # noqa
