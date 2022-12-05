'''                               ,----,.
                             ,'   ,' |
    ,---,                  ,'   .'   |
  .'  .' `\              ,----.'    .'  ,--,         ,---,
,---.'     \             |    |   .'  ,--.'|       ,---.'|
|   |  .`\  |            :    :  |--, |  |,        |   | :
:   : |  '  |  ,--.--.   :    |  ;.' \`--'_        |   | |
|   ' '  ;  : /       \  |    |      |,' ,'|     ,--.__| |
'   | ;  .  |.--.  .-. | `----'.'\   ;'  | |    /   ,'   |
|   | :  |  ' \__\/: . .   __  \  .  ||  | :   .   '  /  |
'   : | /  ;  ," .--.; | /   /\/  /  :'  : |__ '   ; |:  |
|   | '` ,/  /  /  ,.  |/ ,,/  ',-   .|  | '.'||   | '/  '
;   :  .'   ;  :   .'   \ ''\       ; ;  :    ;|   :    :|
|   ,.'     |  ,     .-./\   \    .'  |  ,   /  \   \  /
'---'        `--`---'     `--`-,-'     ---`-'    `----'



2022 wookieware.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0.

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


__author__ = "@netwookie"
__credits__ = ["Rick Kauffman"]
__license__ = "Apache2"
__version__ = "0.1.1"
__maintainer__ = "Rick Kauffman"
__email__ = "rick@rickkauffman.com"
__status__ = "Alpha"

'''
from bson.json_util import dumps
from bson.json_util import loads
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

data_folder = Path()

file_to_open = data_folder / "da5id_deal_report.html"
#Script to get all logs from database
def prep_deals(db):
    cr = '\n'
    # Set filehandle
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('deals_report.html')

    # Get deals
    get_deals = db.deals.find({},{"_id":0,"deal":1,"company":1,"status":1,"thoughts":1,"partner":1,"notes":1,"customer":1,"ope":1,"price":1,"quarter":1,"accountmgr":1})
    json_deals = loads(dumps(get_deals))
    output_from_parsed_template = template.render(deals=json_deals)

    # to save the results
    with open("da5id_deals_report.html", "w") as fh:
        fh.write(output_from_parsed_template)

    fh.close()
    return json_deals
