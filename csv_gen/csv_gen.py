from gooey import Gooey, GooeyParser
import csv, os


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
                working_list.append(row[6])
                eap_data.append(working_list)

    with open(os.path.join(os.getcwd(), 'bracketed_skus.csv'), 'w', newline='') as new_csv:
        data_writer = csv.writer(new_csv)
        for row in eap_data:
            data_writer.writerow(row)

if __name__ == '__main__':
    main()


    # Company --> 100100100|Fastenal XXXXX
    # SiteId --> siteId=100100100
    # ProductSku --> productSku=63123
    # BracketSku --> 63123[1]