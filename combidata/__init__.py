from combidata.classes.data_generator import DataGenerator
from combidata.classes.process import Process
from combidata.processes.combine import combine
from combidata.processes.form import form
from combidata.processes.genetate import generate



ST_COMBINE = Process("ST_COMBINE", combine)
ST_GENERATE = Process("ST_GENERATE", generate)
ST_FORM = Process("ST_FORM", form)





