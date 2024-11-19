
### 1. Directory Structure

```
/server
  /schemas
    __init__.py
    base.py          # Base schemas and common properties
    user.py          # User schema
    review.py        # Review schema
    customer_usage.py# Customer Usage schema
    place.py         # Place schema
```

**base.py**

```python
# server/schemas/base.py
from pydantic import BaseModel
from datetime import datetime

class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
```

**user.py**

```python
# server/schemas/user.py
from .base import BaseSchema
from typing import List, Optional
from datetime import datetime

class UserBase(BaseSchema):
    username: str
    dob: Optional[datetime] = None
    country: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    reviews: List['Review'] = []
    usages: List['CustomerUsage'] = []
```

**review.py**

```python
# server/schemas/review.py
from .base import BaseSchema
from typing import Optional

class ReviewBase(BaseSchema):
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    place_id: int

class Review(ReviewBase):
    id: int
    user_id: int
    place_id: int
```

**customer_usage.py**

```python
# server/schemas/customer_usage.py
from .base import BaseSchema
from datetime import datetime

class CustomerUsageBase(BaseSchema):
    request_made: str
    timestamp: datetime

class CustomerUsageCreate(CustomerUsageBase):
    pass

class CustomerUsage(CustomerUsageBase):
    id: int
    user_id: int
```

**place.py**

```python
# server/schemas/place.py
from .base import BaseSchema
from typing import List

class PlaceBase(BaseSchema):
    # Define necessary fields like name, location, etc.
    name: str

class PlaceCreate(PlaceBase):
    pass

class Place(PlaceBase):
    id: int
    reviews: List['Review'] = []
```

**__init__.py**

```python
# server/schemas/__init__.py
from .user import User, UserCreate, UserBase
from .review import Review, ReviewCreate, ReviewBase
from .customer_usage import CustomerUsage, CustomerUsageCreate, CustomerUsageBase
from .place import Place, PlaceCreate, PlaceBase
```