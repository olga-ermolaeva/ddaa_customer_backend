# ddaa_customer_backend
Python app that customers can deploy on their own server, put their data into this app, track annotation progress and update the database with data from verifiers. 

Inner functions:
load_data(path)
make_batches()
update_annotation_tracking() - update data about labeling pro
update_labels(labels_mapping)
export_dataset(export_path, export_format)

GET: None

POST:
UpdateAnnotation() - receiving annotated data from verifier, then updating annotation results and annotation tracking.

requests: 
POST recieveImageBatch() - отправить на фронт аннотатора изображения
