' Backup copy - not automatically added to exported Excel file - exists in personal macro workbook '

Sub Format_H3()
    Dim wb As Workbook
    Dim ts As TableStyle, el As TableStyleElement
    Dim b As Variant
    Dim ws As Worksheet, lo As ListObject
    Dim shp As Shape, cell As Range
    Const padH As Double = 4
    Const padV As Double = 4

    Set wb = ActiveWorkbook
    Application.ScreenUpdating = False

    '— (Re)create HeroesTable style —
    On Error Resume Next: wb.TableStyles("HeroesTable").Delete: On Error GoTo 0
    Set ts = wb.TableStyles.Add("HeroesTable")
    With ts.TableStyleElements(xlWholeTable)
        For Each b In Array(xlEdgeLeft, xlEdgeTop, xlEdgeBottom, xlEdgeRight, xlInsideVertical, xlInsideHorizontal)
            With .Borders(b)
                .LineStyle = xlContinuous: .Weight = xlThin: .Color = RGB(166, 166, 166)
            End With
        Next b
        .Font.Color = vbWhite
    End With
    Set el = ts.TableStyleElements(xlHeaderRow)
    With el
        .Interior.Pattern = xlSolid: .Interior.Color = RGB(100, 100, 100)
        .Font.Bold = True
    End With
    With ts.TableStyleElements(xlRowStripe1).Interior
        .Pattern = xlSolid: .Color = RGB(30, 30, 30)
    End With
    With ts.TableStyleElements(xlRowStripe2).Interior
        .Pattern = xlSolid: .Color = RGB(45, 45, 45)
    End With

    '— Main loop: one sheet at a time —
    For Each ws In wb.Worksheets
        ' select only this sheet
        ws.Select Replace:=True

        ' window & cell defaults per sheet
        ActiveWindow.Zoom = 80
        ActiveWindow.TabRatio = 0.9
        ActiveWindow.DisplayHeadings = False

        ' dark background
        ws.Cells.Interior.Color = RGB(32, 32, 32)

        ' build or get table
        If ws.ListObjects.Count = 0 Then
            Set lo = ws.ListObjects.Add(xlSrcRange, ws.UsedRange, , xlYes)
            lo.Name = "tbl_" & ws.Name
        Else
            Set lo = ws.ListObjects(1)
        End If

        ' apply style
        lo.TableStyle = "HeroesTable"
        lo.HeaderRowRange.Font.Color = vbWhite
        lo.Range.Interior.Pattern = xlNone

        ' font size
        lo.DataBodyRange.Font.Size = 12

        ' first-column font
        If Not lo.DataBodyRange Is Nothing Then
            lo.DataBodyRange.Font.Size = 12
        End If

        ' conditional formatting on A
        ws.Columns("A").FormatConditions.Delete
        ws.Range("A1").FormatConditions.Delete
        With ws.Range("A1").FormatConditions.Add(xlExpression, , "=TRUE")
            .Interior.Color = RGB(105, 106, 72): .StopIfTrue = True
        End With
        With ws.Columns("A").FormatConditions.Add(xlExpression, , "=AND(ROW()>1,MOD(ROW(),2)=1)")
            .Interior.Color = RGB(53, 53, 35): .StopIfTrue = True
        End With
        With ws.Columns("A").FormatConditions.Add(xlExpression, , "=AND(ROW()>1,MOD(ROW(),2)=0)")
            .Interior.Color = RGB(35, 36, 24): .StopIfTrue = True
        End With

        ' Color-based conditional formatting for Heroes and Towns sheets
        If ws.Name = "Heroes" Or ws.Name = "Towns" Or ws.Name = "Town Events" Then
            Dim colorCol As Integer
            Dim dataRange As Range
            Dim colorColLetter As String

            If Not lo.DataBodyRange Is Nothing Then
                If ws.Range("A2").Value = "No data" Then GoTo SkipColorFormatting

                ' Find the Color column
                On Error Resume Next
                colorCol = lo.ListColumns("Color").Index
                On Error GoTo 0

                If colorCol > 0 Then
                    ' Convert column number to letter
                    colorColLetter = Split(lo.ListColumns("Color").Range.Cells(1).Address, "$")(1)

                    ' Clear existing conditional formatting from the data range (excluding column A)
                    If lo.DataBodyRange.Columns.Count > 1 Then
                        lo.DataBodyRange.Offset(0, 1).Resize(lo.DataBodyRange.Rows.Count, lo.DataBodyRange.Columns.Count - 1).FormatConditions.Delete
                    End If

                    ' Set data range excluding column A (starting from column B)
                    Set dataRange = lo.DataBodyRange.Offset(0, 1).Resize(lo.DataBodyRange.Rows.Count, lo.DataBodyRange.Columns.Count - 1)

                    ' Add conditional formatting for each color
                    ' Red - Dark desaturated red
                    With dataRange.FormatConditions.Add(xlExpression, , "=$" & colorColLetter & "2=""Red""")
                        .Interior.Color = RGB(75, 30, 30): .StopIfTrue = True
                    End With

                    ' Blue - Dark desaturated blue
                    With dataRange.FormatConditions.Add(xlExpression, , "=$" & colorColLetter & "2=""Blue""")
                        .Interior.Color = RGB(30, 30, 75): .StopIfTrue = True
                    End With

                    ' Tan - Dark desaturated tan
                    With dataRange.FormatConditions.Add(xlExpression, , "=$" & colorColLetter & "2=""Tan""")
                        .Interior.Color = RGB(60, 52, 37): .StopIfTrue = True
                    End With

                    ' Green - Dark desaturated green
                    With dataRange.FormatConditions.Add(xlExpression, , "=$" & colorColLetter & "2=""Green""")
                        .Interior.Color = RGB(30, 60, 30): .StopIfTrue = True
                    End With

                    ' Orange - Dark desaturated orange
                    With dataRange.FormatConditions.Add(xlExpression, , "=$" & colorColLetter & "2=""Orange""")
                        .Interior.Color = RGB(75, 45, 22): .StopIfTrue = True
                    End With

                    ' Purple - Dark desaturated purple
                    With dataRange.FormatConditions.Add(xlExpression, , "=$" & colorColLetter & "2=""Purple""")
                        .Interior.Color = RGB(60, 30, 60): .StopIfTrue = True
                    End With

                    ' Teal - Dark desaturated teal
                    With dataRange.FormatConditions.Add(xlExpression, , "=$" & colorColLetter & "2=""Teal""")
                        .Interior.Color = RGB(30, 60, 60): .StopIfTrue = True
                    End With

                    ' Pink - Dark desaturated pink
                    With dataRange.FormatConditions.Add(xlExpression, , "=$" & colorColLetter & "2=""Pink""")
                        .Interior.Color = RGB(75, 45, 60): .StopIfTrue = True
                    End With

                    ' Neutral - Dark gray
                    With dataRange.FormatConditions.Add(xlExpression, , "=$" & colorColLetter & "2=""Neutral""")
                        .Interior.Color = RGB(45, 45, 45): .StopIfTrue = True
                    End With
                End If
            End If
        End If

SkipColorFormatting:

        ' align + autofit horizontally
        ws.Range("A1").HorizontalAlignment = xlLeft
        ws.Cells.EntireColumn.AutoFit
        ws.Range("A1").HorizontalAlignment = xlCenter

        ' center and word wrap
        ws.Cells.Select
        With Selection
            .HorizontalAlignment = xlCenter
            .VerticalAlignment = xlCenter
            .WrapText = True
            .Orientation = 0
            .AddIndent = False
            .IndentLevel = 0
            .ShrinkToFit = False
            .ReadingOrder = xlContext
            .MergeCells = False
        End With
        ws.Range("A1").Select

        ' align + autofit horizontally again
        If Not ws.Range("A2").Value = "No data" Then
            ws.Range("A1").HorizontalAlignment = xlLeft
            ws.Cells.EntireColumn.AutoFit
            ws.Range("A1").HorizontalAlignment = xlCenter
        End If

        ' sheet-specific tweaks
        If Not ws.Range("A2").Value = "No data" Then
            If ws.Name = "Heroes" Or ws.Name = "Towns" Or ws.Name = "Town Events" Or ws.Name = "Global Events" _
                Or ws.Name = "Monsters" Or ws.Name = "Artifacts" Or ws.Name = "Campfire" Or ws.Name = "Creature Banks" _
                Or ws.Name = "Garrisons" Then
                Dim colList As Variant, colName As Variant, c As Range
                Select Case ws.Name
                    Case "Heroes"
                        colList = Array("Secondary Skills", "Creatures", "Artifacts", "Biography", "Spells")
                    Case "Towns"
                        colList = Array("Garrison Guards", "Buildings – Built", "Buildings – Disabled", _
                                        "Spells – Always", "Spells – Disabled")
                    Case "Town Events"
                        colList = Array("Message", "Resources", "Players", "Creatures", "Buildings")
                    Case "Global Events"
                        colList = Array("Message", "Resources", "Players")
                    Case "Monsters"
                        colList = Array("Message", "Resources")
                    Case "Artifacts"
                        colList = Array("Guards", "Pickup Conditions", "Message")
                    Case "Campfire"
                        colList = Array("Resources")
                    Case "Creature Banks"
                        colList = Array("Artifacts")
                    Case "Garrisons"
                        colList = Array("Guards")
                End Select

                For Each colName In colList
                    On Error Resume Next
                    For Each c In lo.ListColumns(colName).DataBodyRange.Cells
                        If Len(c.Value) > 0 And c.Value <> "–" Then
                            c.HorizontalAlignment = xlLeft
                            c.Font.Size = 10
                        End If
                    Next
                    On Error GoTo 0
                Next
            End If
        End If

        '–– Monsters-only number format for Quantity & AI Value ––
        If ws.Name = "Monsters" Then
            On Error Resume Next
            lo.ListColumns("Quantity").DataBodyRange.NumberFormat = "#,##0"
            lo.ListColumns("AI Value").DataBodyRange.NumberFormat = "#,##0"
            On Error GoTo 0
        End If

        ' autofit vertically
        If Not ws.Range("A2").Value = "No data" Then
            ws.Cells.EntireRow.AutoFit
        End If

        ' cap any wide columns to 85
        For Each colRange In ws.UsedRange.Columns
            If colRange.ColumnWidth >= 85 Then colRange.ColumnWidth = 85
        Next colRange

        ' make Heroes-only tweaks (part 2)
        If ws.Name = "Heroes" Then
            ' center & scale pictures, bump only too-small rows
            For Each shp In ws.Shapes
                If shp.Type = msoPicture Then
                    shp.ScaleHeight 1, msoTrue, msoScaleFromTopLeft
                    shp.ScaleWidth 1, msoTrue, msoScaleFromTopLeft
                    shp.LockAspectRatio = msoTrue
                    shp.Placement = xlMove
                    Set cell = shp.TopLeftCell
                    shp.Width = cell.Width - padH
                    If cell.RowHeight < shp.Height + padV Then cell.RowHeight = shp.Height + padV
                    shp.Left = cell.Left + padH / 2
                    shp.Top = cell.Top + (cell.RowHeight - shp.Height) / 2
                End If
            Next shp

            ' format Experience column with commas and "XP" suffix
            On Error Resume Next
            For Each cell In lo.ListColumns("Experience").DataBodyRange.Cells
                If IsNumeric(cell.Value) And Len(cell.Value) > 0 Then
                    cell.Value = Format(cell.Value, "#,##0") & " XP"
                End If
            Next
            On Error GoTo 0
        End If

        ' fill empty cells in the table with centered en dashes and apply mid-gray color
        For Each r In lo.DataBodyRange.Cells
            If IsEmpty(r.Value) Or r.Value = "" Then
                r.Value = "–"
                r.Font.Color = RGB(150, 150, 150)  ' Mid-gray color
                r.HorizontalAlignment = xlCenter   ' Ensure en dashes are centered
            ElseIf r.Value = "–" Then
                ' Apply gray color to existing en dashes (for subsequent runs)
                r.Font.Color = RGB(150, 150, 150)
                r.HorizontalAlignment = xlCenter   ' Ensure en dashes are centered
            End If
        Next r

        ' freeze & reselect A1
        ActiveWindow.SplitRow = 1
        ActiveWindow.SplitColumn = 1
        ActiveWindow.FreezePanes = True
        ws.Range("A1").Select
    Next ws

    ' Apply tab color to specified sheets
    Dim tabsToColor As Variant: tabsToColor = Array("Seer\'s Hut", "Quest Objects", "Event Objects", _
        "Border Objects", "Dwellings", "Mines & Warehouses", "Interactive", "Simple Objects", "Text")

    For Each b In tabsToColor
        With wb.Sheets(b).Tab
            .ThemeColor = xlThemeColorLight1
            .TintAndShade = 0.499984740745262
        End With
    Next b

    ' back to first sheet
    wb.Worksheets(1).Select
    wb.Worksheets(1).Range("A1").Select
    wb.Save
    Application.ScreenUpdating = True
End Sub
