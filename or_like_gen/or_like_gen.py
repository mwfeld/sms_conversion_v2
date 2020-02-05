from gooey import Gooey, GooeyParser
import os, csv


@Gooey(requires_shell=False)
def main():
    parser = GooeyParser(description="SQL OR LIKE BRANCH GEN V0.1")
    parser.add_argument('branch_list_file', widget='FileChooser',
        help="Please select the branch list text file...")
    args = parser.parse_args()
    branch_list_path = args.branch_list_file
    
    with open(branch_list_path, 'r') as f:
        text_list = []
        flag = True
        for branch in f:
            if flag:
                text_list.append("'%{}'\n".format(branch.strip()))
                flag = False
            else:
                text_list.append("OR name LIKE '%{}'\n".format(branch.strip()))

    with open(branch_list_path, 'w') as f:
        for text in text_list:
            f.write(text)

if __name__ == '__main__':
    main()