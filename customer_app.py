import os
import io
import sys
import glob

import pandas as pd
from sklearn.utils import shuffle

from typing import Union, List, Any

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.logger import logger
from pydantic import BaseSettings

from PIL import Image

# variables
data_path = 'dataset2'
task_description = 'Description' # TODO
classes =  ['sunrise', 'shine', 'cloudy', 'rain']
batch_size = 30

# all data manipulations functionality
#df.columns = ['imagepath', 'imageid', 'status', 'label1', 'label2']
status_types = ['clear', 'in_progress', 'first_done', 'completed']

class DatasetCreator():
    def __init__(self) -> None:
        self.df = self.load_data(data_path)
        self.df = self.shuffle_data(self.df)

    def load_data(self, data_path:str):
        #find all image paths
        image_paths = glob.glob(f'{data_path}/*')[:200]
        #create table
        df = pd.DataFrame(image_paths)
        df.columns = ['imagepath']
        df['status'] = 'clear'
        df['label1'] = None
        df['label2'] = None
        return df

    def shuffle_data(self, df):
        df = self.df
        df = shuffle(df)
        return df
    
    def get_image_batch(self):
        df = self.df
        df_have_first = df[ df['status'] == 'first_done']
        if df_have_first.shape[0] > batch_size:
            batch_df = df_have_first.head(batch_size)
        else:
            df_clear = df[ df['status'] == 'clear']
            if df_have_first.shape[0] != 0:
                df_clear_batch = df_clear.head(batch_size-df_have_first.shape[0])
                batch_df = pd.concat([df_have_first, df_clear_batch])
            else:
                batch_df = df_clear.head(batch_size)
        batch_df['imagepath']
        imagespaths = batch_df['imagepath'].tolist()
        #images = [bytes(open(filename, 'rb').read()) for filename in imagespaths]
        #images = []
        #for imp in imagespaths:
        #    with open(imp, 'rb') as f:
        #        byte_im = f.read()
        #        images+= byte_im
        batch_data = zip( imagespaths,  batch_df['imagepath'].index.values.tolist())
        return [{'imageid' : index, 'imagepath' : image} for image,index in batch_data]
        #return [{'imageid' : index, 'image' : bytearray(open(filename, 'rb').read())} for filename,index in batch_data]
        #return [{'imageid' : index, 'image' : io.BytesIO(open(filename, 'rb').tobytes())} for filename,index in batch_data]

    def update_annotation_tracking(self, annotation_result):
        for sample in annotation_result:
            label = sample['label']
            imageid = sample['imageid']
            status = self.df.loc[imageid]['status']
            if status == 'clear':
                self.df.loc[imageid]['status'] = 'first_done'
            if status == 'first_done':
                self.df.loc[imageid]['status'] = 'completed'


    def update_labels(self, annotation_result):
        for sample in annotation_result:
            label = sample['label']
            imageid = sample['imageid']
            if self.df.loc[imageid]['status'] == 'first_done':
                self.df.loc[imageid]['label2'] = label
            else:
                self.df.loc[imageid]['label1'] = label


    def export_dataset():
        pass


def test_dataset_creator():
    dataset = DatasetCreator()
    annotation_result = [{'imageid': 10, 'label': 1}, {'imageid': 20, 'label': 3}]
    dataset.update_labels(annotation_result)
    dataset.update_annotation_tracking(annotation_result)

    dataset.get_image_batch()


# Data nodels
class AnnotationSample(BaseModel):
    imageid: str
    label: int

class Annotation(BaseModel):
    items: List[AnnotationSample]

class Sample(BaseModel):
    imageid: str
    image: Any # TODO what type should be here?

class SampleList(BaseModel):
    samples: List[Sample]

# API
app = FastAPI()
app.mount("/dataset2", StaticFiles(directory="dataset2"), name="dataset2")
dataset = DatasetCreator()


#@app.get("/image_batch", response_model=SampleList, response_model_exclude_unset=True)
@app.get("/image_batch")
async def send_image_batch():
    items = dataset.get_image_batch()
    return {'samples': items} #here should be generated image batch # OR 

@app.get("/description")
async def send_task_description():
    return {'description' : task_description}

@app.get("/classes")
async def send_classes():
    return {'classes' : classes}

# TODO add DatasetCreator.update_labels() call
@app.post("/annotation_result")
async def update_annotation(data: Annotation):
    dataset.update_labels(data)
    dataset.update_annotation_tracking(data)
    return 0


# run app on public URL

if __name__ == "__main__":
    uvicorn.run(app)
    #uvicorn.run(app, host="192.168.1.23", port=8000)
    #uvicorn.run(app, host="0.0.0.0", port=8000)