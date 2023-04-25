from .crud_user import user
from .crud_run import run
from .crud_template import template
from .crud_sample import sample
from .crud_consensus import consensus
from .crud_coverage import coverage


# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
