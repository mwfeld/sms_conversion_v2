from gooey import Gooey, GooeyParser
import csv, os
import re

@Gooey(requires_shell=False)
def main():
    parser = GooeyParser(description="BRACKET SKU CSV GEN")
    parser.add_argument('branch_list_file', widget='FileChooser',
        help="Please select the csv exported from EAP...")
    args = parser.parse_args()
    csv_path = args.branch_list_file
    
    eap_data = [['Company', 'SiteId', 'ProductSku', 'BracketSku']]

    with open(csv_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        flag = True
        for row in reader:
            if flag:
                flag = False
                continue
            else:
                working_list = []
                working_list.append('{}|{}'.format(row[2][3:], row[0]))
                working_list.append('siteId={}'.format(row[4][3:]))
                working_list.append('productSku={}'.format(row[5]))
                working_list.append(format_bracketed_sku(row[6]))
                eap_data.append(working_list)

    with open(os.path.join(os.getcwd(), 'bracketed_skus.csv'), 'w', newline='') as new_csv:
        data_writer = csv.writer(new_csv)
        for row in eap_data:
            data_writer.writerow(row)

def strip_space_brackets(sku):
    p_sku_space = re.compile(r'(^.*)(\[\d*\]$)')
    if re.search(p_sku_space, sku):
        re_result = re.search(p_sku_space, sku)
        stripped_sku = '{}{}'.format(re_result.group(1).strip(), re_result.group(2))
        return stripped_sku
    else:
        return sku

def vendpack_to_upper(sku):
    p_sku_v = re.compile(r'^.*(v)\d*\[\d*\]$')
    if re.match(p_sku_v, sku):
        match_index = re.match(p_sku_v, sku).start(1)
        sku_upper_v = ''.join([
            sku[:match_index],
            sku[match_index].upper(),
            sku[match_index + 1:]])
        return sku_upper_v
    else:
        return sku

def format_bracketed_sku(sku):
    formatted_sku = strip_space_brackets(sku)
    formatted_sku = vendpack_to_upper(formatted_sku)
    return formatted_sku


if __name__ == '__main__':
    main()


    # Company --> 100100100|Fastenal XXXXX
    # SiteId --> siteId=100100100
    # ProductSku --> productSku=63123
    # BracketSku --> 63123[1]