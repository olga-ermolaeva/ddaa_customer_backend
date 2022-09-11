# ddaa_customer_backend
Python app that customers can deploy on their own server, put their data into this app, track annotation progress and update the database with data from verifiers. 

Inner functions:
* load_data(path)
* make_batches()
* update_annotation_tracking() - update data about labeling pro
* update_labels(labels_mapping)
* export_dataset(export_path, export_format)


GET: 
* /image_batch - отправить на фронт аннотатора изображения. Return example: {'samples': [{'imageid': 0, 'imagepath': 'dataset2/cloudy6.jpg'}, {'imageid': 81, 'imagepath': 'dataset2/cloudy235.jpg'}]}
* /description - отправить описание задачи / руководство по выполнению. Return string.
* /classes - отправить названия классов которые будут на кнопках в интерфейсе аннотации. Return list of strings
* /dataset2/*.jpg - Доступ к статичным файлам в датасете. По imagepath полученному от /image_batch можно скачать изображение.

POST:
* /annotation_result - receiving annotated data from verifier, then updating annotation results and annotation tracking. annotated data example: [{'imageid': 10, 'label': 1}, {'imageid': 20, 'label': 3}]
 
