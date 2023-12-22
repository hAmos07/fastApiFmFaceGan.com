import os
import uuid
import zipfile

from sqlalchemy import Column, String, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from fmfacegan.config import settings
from fmfacegan.database.create import record_xml_create

BASE_DIR = os.path.dirname(os.path.abspath(__name__))
db_path = os.path.join(BASE_DIR, 'fmfacegan', 'database', 'DB')
if not os.path.exists(db_path):
    os.makedirs(db_path)

Base = declarative_base()
engine = create_engine(settings.face_db, connect_args={'check_same_thread': False}, echo=False)

race_list = ('africa', 'asia', 'euro', 'latina')


def crate_models(tablename: str):
    class Regens(Base):
        __tablename__ = tablename
        __table_args__ = {'extend_existing': True}

        file_name = Column(String, primary_key=True)
        used = Column(Boolean)

        def __int__(self, file_name: str, used: bool):
            self.file_name = file_name
            self.used = used

    return Regens


def create_db(db_session):
    if not os.path.exists(settings.face_db_path):
        for race in race_list:
            crate_models(race)
        Base.metadata.create_all(engine)
        load_data_in_db(db_session)


def load_data_in_db(db_session):
    for race in race_list:
        RaceModel = crate_models(race)
        i = 1
        while i <= 100000:
            regen = RaceModel(file_name=f'{i}.png', used=False)
            db_session.add(regen)
            i += 1
    db_session.commit()
    db_session.close()


def get_images_from_db(db_session, data: dict) -> dict:
    records_list = list()
    unic_id = str(uuid.uuid4())
    graphics_archive = f'graphics-{unic_id}.zip'
    tmp_config_xml_file = f'fmfacegan/content/faces/tmp/{unic_id}_config.xml'
    graphics_archive_path = f'fmfacegan/download/{graphics_archive}'

    for race in race_list:
        ids = data[race]
        if len(ids) > 0:
            RaceModel = crate_models(race)
            not_used_images_count = db_session.query(RaceModel).filter(RaceModel.used == 0).count()
            if not_used_images_count > 0:
                images = db_session.query(RaceModel).filter(RaceModel.used == 0).limit(len(ids))
                with zipfile.ZipFile(graphics_archive_path, 'a') as archive:
                    i = 0
                    for img in images:
                        new_file = f'{ids[i]}.png'
                        records_list.append(ids[i])
                        archive.write(f'fmfacegan/content/faces/{race}/{img.file_name}', f'graphics/regens_faces/{new_file}',
                                      compress_type=zipfile.ZIP_DEFLATED)
                        # Change id, 'used': = True
                        used_image = db_session.query(RaceModel).filter(RaceModel.file_name == img.file_name).one()
                        used_image.used = True
                        db_session.add(used_image)
                        i += 1
    db_session.commit()
    if not os.path.exists(graphics_archive_path):
        return {'success': False, 'download_url': f'error'}

    # Create config.xml file
    with open(file=tmp_config_xml_file, mode='w', encoding='UTF-8') as config_file:
        config_file.write(record_xml_create(records_list))
    # Add config.xml file to archive
    with zipfile.ZipFile(graphics_archive_path, 'a') as archive:
        archive.write(tmp_config_xml_file, 'graphics/regens_faces/config.xml', compress_type=zipfile.ZIP_DEFLATED)
    # Delete config.xml file
    os.remove(tmp_config_xml_file)
    return {'success': True, 'download_url': f'/download/{graphics_archive}'}


# create session
def get_db():
    db_session_local = SessionLocal()
    try:
        yield db_session_local
    finally:
        db_session_local.close()


SessionLocal = sessionmaker(bind=engine)
