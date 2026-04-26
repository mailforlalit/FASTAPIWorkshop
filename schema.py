from pydantic import BaseModel, Field
class Task(BaseModel):
    title: str = Field( ... , pattern='^[a-zA-Z0-9_-]+$', description='Title of the task should be alphanumeric and can include space')
    description: str = Field( ... , pattern='^[a-zA-Z0-9_-]+$', description='Description of the task should be alphanumeric and can include space')
    status: str = Field( ... , pattern='^[a-zA-Z0-9_-]+$', description='Status of the task should be alphanumeric and can include space')

