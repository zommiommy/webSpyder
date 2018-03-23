from webSpyder.data_strucutre.linkGraph import LinkGraph
from webSpyder.data_strucutre.webList import WebList
from webSpyder.data_strucutre.distribuitedWebList import DistribuitedWebList

def initialize_data_structure(logger,data_type):
  data_types = {
    "linkGraph":LinkGraph,
    "webList":WebList,
    "distribuitedWebList":DistribuitedWebList
  }
  if  data_type in data_types.keys():
    logger.info("Starting using %s data_type"%data_type)
    return data_types[data_type](logger)
  else:
    logger.error("Error there is no data_type %s , the available one are %s"%(data_type,data_types.keys()))
    raise Exception("Error there is no data_type %s , the avilable one are %s"%(data_type,data_types.keys()))