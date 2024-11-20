import pytest
from streaming import Session, Base, engine

@pytest.fixture(scope='module')
def session():
    # Ensure the tables are created
    Base.metadata.create_all(engine)
    
    # Create a new session
    session = Session()
    yield session
    session.close()



