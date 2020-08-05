Attribute VB_Name = "ģ��11"
Sub draft_work_kai_chen()

Dim P001_current_book_path As String
P001_current_book_path = ThisWorkbook.Path

Dim FSO As Object
Set FSO = CreateObject("Scripting.FileSystemObject")

Dim F001_SETS As Object
Set F001_SETS = FSO.getfolder(P001_current_book_path)

'�����ļ�ϵͳ����������Excel Object Library

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
'��������

Dim counter As Integer

'�ļ�·���ַ���������
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

'��ʼ����
For counter = 2 To 100:

ThisWorkbook.Activate
P001_sheet.Select

TAG_TRIGGER = Cells(counter, "A").Value

If TAG_TRIGGER = "STOP" Then
    Debug.Print "Incident Close"
    MsgBox ("End")
    Exit For
End If
'״̬�����
'ȡֵ����
N001_book_source = Cells(counter, "B").Value
'Դ�ļ�
N001_sheet_source = Cells(counter, "C").Value
'Դ��
N001_book_target = Cells(counter, "E").Value
'Ŀ���ļ�
N001_sheet_target = Cells(counter, "F").Value
'Ŀ���
S001_Sou_C = Cells(counter, "D").Value
'�ֶγ���
S001_COL_SOU = Split(S001_Sou_C, ",")
'�з�
'Debug.Print "SOURCE_COL FROM"
'Debug.Print S001_COL_SOU(0)
S001_Tar_C = Cells(counter, "G").Value
'Ŀ���ֶγ���
S001_COL_TAR = Split(S001_Tar_C, ",")
'�з�
'Debug.Print "TARGET_COL TO"
'Debug.Print S001_COL_TAR(0)
S001_Sou_R_S = Cells(counter, "H").Value
'��ʼ��Χ
S001_Sou_R_E = Cells(counter, "I").Value
'����

For Each F001_item In F001_FILES:
 
 If InStr(F001_item.Name, N001_book_source) > 0 And InStr(F001_item.Name, "$") = 0 And InStr(F001_item.Name, "xls") > 0 And InStr(F001_item.Name, "xlsm") = 0 Then
 Debug.Print F001_item.Name
 'ͨ���ؼ��ֲ���Դ�ļ�
 Set W001_book_source = Application.Workbooks.Open(F001_item.Path)
 Set W001_sheet_source = W001_book_source.Sheets(N001_sheet_source)
 '����Excel���ö���
 End If
 
 If InStr(F001_item.Name, N001_book_target) > 0 And InStr(F001_item.Name, "$") = 0 And InStr(F001_item.Name, "xls") > 0 And InStr(F001_item.Name, "xlsm") = 0 Then
 Debug.Print F001_item.Name
 'ͨ���ؼ��ֲ���Ŀ���ļ�
 Set W001_book_target = Application.Workbooks.Open(F001_item.Path)
 Set W001_sheet_target = W001_book_target.Sheets(N001_sheet_target)
 '����Excel���ö���
 End If

Next


 For m = S001_Sou_R_S To S001_Sou_R_E
 '�����趨��Χ
 For n = LBound(S001_COL_SOU) To UBound(S001_COL_SOU)
 '�����趨�ֶ�
 
 Debug.Print "FROM"
 Debug.Print S001_COL_SOU(n) & m
 '��ӡԴλ��
 W001_book_source.Activate
 W001_sheet_source.Select
 '����Ŀ���ļ�
 
 Cells(m, S001_COL_SOU(n)).Copy
 '����Ŀ��λ��
 
 Debug.Print "TO"
 Debug.Print S001_COL_TAR(n)
 '��ӡĿ��λ��
 
 W001_book_target.Activate
 W001_sheet_target.Select
 'ճ��Ŀ��λ��
 
 'Cells(T001_line_counter, S001_COL_TAR(n)).Paste
 Range(S001_COL_TAR(n) & T001_line_counter).PasteSpecial xlPasteAll
 
 
 '�ۼ�����
 
 Next
 '��Χѭ������
 T001_line_counter = T001_line_counter + 1
 Next
 '�ֶ�ѭ������
 W001_book_source.Save
 W001_book_source.Close
 
 '�ر�Դ�ļ���׼������һ���ļ�
 W001_book_target.Save
 W001_book_target.Close
 '����ճ�����
Next

MsgBox ("Process End")

End Sub
