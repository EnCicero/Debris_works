Attribute VB_Name = "模块11"
Sub draft_work_kai_chen()

Dim P001_current_book_path As String
P001_current_book_path = ThisWorkbook.Path

Dim FSO As Object
Set FSO = CreateObject("Scripting.FileSystemObject")

Dim F001_SETS As Object
Set F001_SETS = FSO.getfolder(P001_current_book_path)

'激活文件系统对象，需引用Excel Object Library

Dim F001_FILES As Object
Set F001_FILES = F001_SETS.Files

Dim F001_item As Object

Dim W001_book_source As Workbook
Dim W001_sheet_source As Worksheet
Dim W001_book_target As Workbook
Dim W001_sheet_target As Worksheet

Dim P001_sheet As Worksheet
Set P001_sheet = ThisWorkbook.Sheets("PARM")

ThisWorkbook.Activate
P001_sheet.Select
'参数表激活

Dim counter As Integer

'文件路径字符串储存器
Dim N001_book_source As String
Dim N001_sheet_source As String
Dim N001_book_target As String
Dim N001_sheet_target As String
Dim S001_Sou_C As String
Dim S001_Tar_C As String
Dim S001_Sou_R_S As Integer
Dim S001_Sou_R_E As Integer
Dim S001_COL_SOU As Variant
Dim S001_COL_TAR As Variant
Dim TAG_TRIGGER As String

Dim T001_line_counter As Integer
T001_line_counter = 2

'起始行数
For counter = 2 To 100:

ThisWorkbook.Activate
P001_sheet.Select

TAG_TRIGGER = Cells(counter, "A").Value

If TAG_TRIGGER = "STOP" Then
    Debug.Print "Incident Close"
    MsgBox ("End")
    Exit For
End If
'状态设计器
'取值过程
N001_book_source = Cells(counter, "B").Value
'源文件
N001_sheet_source = Cells(counter, "C").Value
'源表单
N001_book_target = Cells(counter, "E").Value
'目标文件
N001_sheet_target = Cells(counter, "F").Value
'目标表单
S001_Sou_C = Cells(counter, "D").Value
'字段陈列
S001_COL_SOU = Split(S001_Sou_C, ",")
'切分
'Debug.Print "SOURCE_COL FROM"
'Debug.Print S001_COL_SOU(0)
S001_Tar_C = Cells(counter, "G").Value
'目标字段陈列
S001_COL_TAR = Split(S001_Tar_C, ",")
'切分
'Debug.Print "TARGET_COL TO"
'Debug.Print S001_COL_TAR(0)
S001_Sou_R_S = Cells(counter, "H").Value
'起始范围
S001_Sou_R_E = Cells(counter, "I").Value
'结束

For Each F001_item In F001_FILES:
 
 If InStr(F001_item.Name, N001_book_source) > 0 And InStr(F001_item.Name, "$") = 0 And InStr(F001_item.Name, "xls") > 0 And InStr(F001_item.Name, "xlsm") = 0 Then
 Debug.Print F001_item.Name
 '通过关键字查找源文件
 Set W001_book_source = Application.Workbooks.Open(F001_item.Path)
 Set W001_sheet_source = W001_book_source.Sheets(N001_sheet_source)
 '建立Excel调用对象
 End If
 
 If InStr(F001_item.Name, N001_book_target) > 0 And InStr(F001_item.Name, "$") = 0 And InStr(F001_item.Name, "xls") > 0 And InStr(F001_item.Name, "xlsm") = 0 Then
 Debug.Print F001_item.Name
 '通过关键字查找目标文件
 Set W001_book_target = Application.Workbooks.Open(F001_item.Path)
 Set W001_sheet_target = W001_book_target.Sheets(N001_sheet_target)
 '建立Excel调用对象
 End If

Next


 For m = S001_Sou_R_S To S001_Sou_R_E
 '遍历设定范围
 For n = LBound(S001_COL_SOU) To UBound(S001_COL_SOU)
 '遍历设定字段
 
 Debug.Print "FROM"
 Debug.Print S001_COL_SOU(n) & m
 '打印源位置
 W001_book_source.Activate
 W001_sheet_source.Select
 '激活目标文件
 
 Cells(m, S001_COL_SOU(n)).Copy
 '复制目标位置
 
 Debug.Print "TO"
 Debug.Print S001_COL_TAR(n)
 '打印目标位置
 
 W001_book_target.Activate
 W001_sheet_target.Select
 '粘贴目标位置
 
 'Cells(T001_line_counter, S001_COL_TAR(n)).Paste
 Range(S001_COL_TAR(n) & T001_line_counter).PasteSpecial xlPasteAll
 
 
 '累计行数
 
 Next
 '范围循环结束
 T001_line_counter = T001_line_counter + 1
 Next
 '字段循环结束
 W001_book_source.Save
 W001_book_source.Close
 
 '关闭源文件，准备打开下一个文件
 W001_book_target.Save
 W001_book_target.Close
 '保存粘贴结果
Next

MsgBox ("Process End")

End Sub
