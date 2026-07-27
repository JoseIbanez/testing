import logging
from finance.yfin.main_kpi import check_lateral_box

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


#checker = check_lateral_box("SAP.DE")
checker = check_lateral_box("MRL.MC")
