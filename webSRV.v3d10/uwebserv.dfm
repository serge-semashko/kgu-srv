object HTTPSRVForm: THTTPSRVForm
  Left = 342
  Top = 115
  Caption = 'WEB srv'
  ClientHeight = 749
  ClientWidth = 1028
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -10
  Font.Name = 'MS Sans Serif'
  Font.Style = []
  OldCreateOrder = False
  OnClose = FormClose
  OnCreate = FormCreate
  PixelsPerInch = 96
  TextHeight = 13
  object Panel1: TPanel
    Left = 0
    Top = 0
    Width = 1028
    Height = 200
    Align = alTop
    TabOrder = 0
    object SpeedButton1: TSpeedButton
      Left = 13
      Top = 13
      Width = 27
      Height = 27
      Glyph.Data = {
        76010000424D7601000000000000760000002800000020000000100000000100
        04000000000000010000120B0000120B00001000000000000000000000000000
        800000800000008080008000000080008000808000007F7F7F00BFBFBF000000
        FF0000FF000000FFFF00FF000000FF00FF00FFFF0000FFFFFF003FFFFFFFFFFF
        FFFF33333333333FFFFF3FFFFFFFFF00000F333333333377777F33FFFFFFFF09
        990F33333333337F337F333FFFFFFF09990F33333333337F337F3333FFFFFF09
        990F33333333337FFF7F33333FFFFF00000F3333333333777773333333FFFFFF
        FFFF3FFFFF3333333F330000033FFFFF0FFF77777F3333337FF30EEE0333FFF0
        00FF7F337FFF333777FF0EEE00033F00000F7F33777F3777777F0EEE0E033000
        00007FFF7F7FF777777700000E00033000FF777773777F3777F3330EEE0E0330
        00FF337FFF7F7F3777F33300000E033000FF337777737F37773333330EEE0300
        03FF33337FFF77777333333300000333333F3333777773333333}
      NumGlyphs = 2
      OnClick = SpeedButton1Click
    end
    object URLED: TEdit
      Left = 7
      Top = 52
      Width = 507
      Height = 21
      TabOrder = 0
      Text = 'http://nucloweb.jinr.ru/kgu/Cache/get_data.php?callback=?'
    end
    object kgu1stdtxt: TStaticText
      Left = 531
      Top = 26
      Width = 204
      Height = 23
      AutoSize = False
      BevelKind = bkSoft
      BorderStyle = sbsSunken
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = 'MS Sans Serif'
      Font.Style = []
      ParentFont = False
      TabOrder = 1
    end
    object kgu1freqtxt: TStaticText
      Left = 531
      Top = 50
      Width = 203
      Height = 23
      AutoSize = False
      BevelKind = bkSoft
      BorderStyle = sbsSunken
      Caption = 'kgu1freqtxt'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = 'MS Sans Serif'
      Font.Style = []
      ParentFont = False
      TabOrder = 2
    end
    object kgu2stdtxt: TStaticText
      Left = 740
      Top = 26
      Width = 203
      Height = 23
      AutoSize = False
      BevelKind = bkSoft
      BorderStyle = sbsSunken
      Caption = 'kgu2freqtxt'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = 'MS Sans Serif'
      Font.Style = []
      ParentFont = False
      TabOrder = 3
    end
    object kgu2freqtxt: TStaticText
      Left = 739
      Top = 50
      Width = 204
      Height = 23
      AutoSize = False
      BevelKind = bkSoft
      BorderStyle = sbsSunken
      Caption = 'kgu2freqtxt'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clBlack
      Font.Height = -15
      Font.Name = 'MS Sans Serif'
      Font.Style = []
      ParentFont = False
      TabOrder = 4
    end
    object Memo1: TMemo
      Left = 1
      Top = 91
      Width = 1026
      Height = 108
      Align = alBottom
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Height = -11
      Font.Name = 'MS Sans Serif'
      Font.Style = []
      Lines.Strings = (
        'Memo1')
      ParentFont = False
      TabOrder = 5
    end
  end
  object Memo2: TMemo
    Left = 0
    Top = 200
    Width = 1028
    Height = 286
    Align = alTop
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -11
    Font.Name = 'MS Sans Serif'
    Font.Style = []
    ParentFont = False
    TabOrder = 1
  end
  object Memobody: TMemo
    Left = 0
    Top = 486
    Width = 1028
    Height = 244
    Align = alClient
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -11
    Font.Name = 'MS Sans Serif'
    Font.Style = []
    Lines.Strings = (
      'Memobody')
    ParentFont = False
    TabOrder = 2
  end
  object StatusBar1: TStatusBar
    Left = 0
    Top = 730
    Width = 1028
    Height = 19
    Panels = <
      item
        Bevel = pbRaised
        Text = '1'
        Width = 300
      end
      item
        Text = '2'
        Width = 300
      end
      item
        Text = '3'
        Width = 300
      end
      item
        Text = '4'
        Width = 300
      end>
  end
  object ApplicationEvents1: TApplicationEvents
    OnMinimize = ApplicationEvents1Minimize
    Left = 352
    Top = 16
  end
  object PopupMenu1: TPopupMenu
    Left = 656
    Top = 24
    object Restore1: TMenuItem
      Caption = 'Restore'
      OnClick = Restore1Click
    end
    object Minimize1: TMenuItem
      Caption = 'Minimize'
    end
    object quit1: TMenuItem
      Caption = 'quit'
      OnClick = quit1Click
    end
    object Restart1: TMenuItem
      Caption = 'Restart'
      OnClick = Restart1Click
    end
  end
  object restart_apptmr: TTimer
    Interval = 6000000
    OnTimer = restart_apptmrTimer
    Left = 540
    Top = 128
  end
  object writewebfilesTimer: TTimer
    Interval = 4000
    OnTimer = SpeedButton1Click
    Left = 368
    Top = 128
  end
  object insat_timer: TTimer
    Interval = 3000
    OnTimer = insat_timerTimer
    Left = 200
    Top = 120
  end
  object mac30Timer: TTimer
    Interval = 3000
    OnTimer = mac30TimerTimer
    Left = 144
    Top = 136
  end
  object tangoTimer: TTimer
    Interval = 2000
    OnTimer = tangoTimerTimer
    Left = 264
    Top = 200
  end
end
