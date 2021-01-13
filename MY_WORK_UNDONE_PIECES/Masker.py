import os

#set file_list as list
def DIF000_ls_target_file(Filename_key,Filetype_key,Exclude_key):
    for item in os.walk(os.getcwd()):
        DIF001_FC_file_list=item[2]
    DIF001_FC_file_list=[x if Filename_key in x and Filetype_key in x and Exclude_key not in x  else "@N" for x in DIF001_FC_file_list]
    while True:
        try:
            DIF001_FC_file_list.remove("@N")
            print("@N MV")
        except:
            print("@N OFF")
            break
    return DIF001_FC_file_list
 
def FIL001_cat_file_columns(file_name,spliter):
    with open("".join([os.getcwd(),"\\",file_name]),"r") as FIL001_File:
        FIL001_Columns_Lines=FIL001_File.readline().replace("\n","").replace("\r","")#清理换行符
        FIL002_Columns_Lables=FIL001_Columns_Lines.split(spliter)#切分
        return FIL002_Columns_Lables

def FMC001_create_blank_container(file_name):
    FMC001_create_blank_container_path="".join([os.getcwd(),"\\MASK_",file_name])
    with open(FMC001_create_blank_container_path,"a+") as FIL001_File:
        FIL001_File.seek(0)
        FIL001_File.truncate()
        FIL001_File.close()
    return "".join(["MASK_",file_name])

    
Category_policy={"CUST_NAME":"C0_ALL",
             "PRIMARY_ID_NO":"C1_SFZ",
             "CUST_NAME_ENG":"H1_HEX"
             }

def FMD001_get_tar_columns(columns_list,target_list,Category_policy):
    FMD001_column_dict_method=dict(zip(columns_list,len(columns_list)*[""]))
    for FMD001_target_item in target_list:
        print("{} : {}".format(FMD001_target_item,FMD001_target_item))
        try:
            FMD001_column_dict_method[FMD001_target_item]=Category_policy[FMD001_target_item]
        except:
            FMD001_column_dict_method[FMD001_target_item]="C0_ALL"
    print(FMD001_column_dict_method)
    FMD001_index=[]
    for i in range(len(columns_list)):
        FMD001_index.append(i)
    FMD001_column_dict_index=dict(zip(columns_list,FMD001_index))
    FMD001_column_dict=dict() 
    for FMD001_target_item in target_list:
        print("{} : {}".format(FMD001_target_item,FMD001_target_item))
        FMD001_item_dict={FMD001_column_dict_index[FMD001_target_item]:FMD001_column_dict_method[FMD001_target_item]}
        FMD001_column_dict.update(FMD001_item_dict)
    return FMD001_column_dict    

def FMM001_whole_mask_tag_C0_ALL(target_string,mask_char="*"):
    target_string=len(target_string)*mask_char
    return target_string
    
def FMM001_whole_mask_tag_C1_SFZ(target_string,mask_char="*",left_margin=6,right_margin=1):
    FMM001_margin_string_left=target_string[0:left_margin]
    #print(FMM001_margin_string_left)
    FMM001_margin_string_right=target_string[-right_margin:]
    #print(FMM001_margin_string_right)
    FMM001_margin_string_mid=target_string[left_margin:-right_margin]
    #print(FMM001_margin_string_mid)
    FMM001_margin_string_mid=len(FMM001_margin_string_mid)*mask_char
    #print(FMM001_margin_string_mid)
    FMM002_margin_string="".join([FMM001_margin_string_left,FMM001_margin_string_mid,FMM001_margin_string_right])
    return FMM002_margin_string

def FMM001_whole_mask_tag_H1_HEX(target_string,shift_num=17):
    FMM001_margin_string=[]
    for index,char_item in enumerate(target_string):
        FMM001_margin_string.append(hex(ord(char_item)+shift_num))
    FMM001_margin_string=''.join(FMM001_margin_string)
    return FMM001_margin_string


# coversion to pbkdf2：sha256
def FMM001_whole_mask_tag_H1_HAS(target_string,method_parm="pbkdf2:sha256",salt_length_parm=8):
    FMM001_margin_string=generate_password_hash(target_string,method=method_parm,salt_length=salt_length_parm)[18:]
    return FMM001_margin_string

    
#Middle set
Masking_theory={"C0_ALL":FMM001_whole_mask_tag_C0_ALL,
                "C1_SFZ":FMM001_whole_mask_tag_C1_SFZ,
                "H1_HEX":FMM001_whole_mask_tag_H1_HEX,
                "H1_HAS":FMM001_whole_mask_tag_H1_HAS
                }
        
def FMF001_file_wrtie(source_file,target_file,policy_dict,Masking_theory,spliter):
    FMF001_source_file="".join([os.getcwd(),"\\",source_file])
    FMF001_target_file="".join([os.getcwd(),"\\",target_file])
    with open(FMF001_source_file,"r") as FIL001_File:
        FMF001_line_column=FIL001_File.readline()
        FMF001_line_column_num=len(FMF001_line_column.split(spliter))
        with open(FMF001_target_file,"w") as FIL002_File:
            FIL002_File.seek(0)
            FIL002_File.truncate()
            FIL002_File.writelines(FMF001_line_column)
            #FIL002_File.writelines("\n\r")
            FMF001_line_process="default"
            while len(FMF001_line_process)>0:
                FMF001_line_process=FIL001_File.readline()
                if len(FMF001_line_process)>0 and len(FMF001_line_process.split(spliter))==FMF001_line_column_num:
                    FMF001_line_process_list=FMF001_line_process.split(spliter)
                    FMF001_mask_key=list(policy_dict.keys())
                    for keys_tri in FMF001_mask_key:
                        mask_string=FMF001_line_process_list[keys_tri]
                        #
                        try:
                            method_key=policy_dict[keys_tri]
                        except:
                            method_key="C0_ALL"
                        masking_method=Masking_theory[method_key]
                        print(Masking_theory[policy_dict[keys_tri]])
                        mask_string=masking_method(mask_string)
                        FMF001_line_process_list[keys_tri]=mask_string
                    FMF001_line_process=spliter.join(FMF001_line_process_list)
                    FIL002_File.writelines(FMF001_line_process)
                    FIL002_File.writelines("\n")
                    FIL002_File.flush()
                else:
                    pass
            FIL002_File.close()
    FIL001_File.close()
    return True
def PSS001_list_key_word(columns_list,involve_key,white_key):
    target_list=[]
    for item_l1 in columns_list:
        l2_tag=False
        l3_tag=False
        for item_l2 in involve_key:
            print("{} in {}".format(item_l2.upper(),item_l1.upper()))
            if item_l2.upper() in item_l1.upper():
                l2_tag=True
                print("black hit")
            for item_l3 in white_key:
                print("{} in {}".format(item_l3.upper(),item_l1.upper()))
                if item_l3.upper() in item_l1.upper() and l2_tag==True:
                    l3_tag=True
                    print("white hit")
        if l2_tag==True and l3_tag==False:
            print("ALL HIT")
            target_list.append(item_l1)
    return target_list


             
if __name__=="__main__":
    local_file_list=DIF000_ls_target_file("RCNCON23",".txt","MASK_")
    
    Black_key=["name","phone","address","primary","id"]
    White_key=["PARTY_ID","SOL_ID"]
    
    Category_policy={"account_num":"C1_SFZ",
                     "bu_desc":"C1_SFZ",
                     "acct_loan_grade":"H1_HEX"
                     }
    
    for files in local_file_list:
        containers=FMC001_create_blank_container(files)
        columns_set=FIL001_cat_file_columns(files,"|")
        target_key_set=PSS001_list_key_word(columns_set,Black_key,White_key)
        policy_dict=FMD001_get_tar_columns(columns_set,target_key_set,Category_policy)
        FMF001_file_wrtie(files,containers,policy_dict,Masking_theory,"|")
