unit uwebserv;
//fdgsdfgsdf
interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls, Buttons, ExtCtrls, HTTPSend,  blcksock, winsock, Synautil,strutils,
  AppEvnts, Menus,inifiles,das_const,ipcthrd,
  TeEngine, Series, TeeProcs, Chart, VclTee.TeeGDIPlus;


type
  THTTPSRVForm = class(TForm)
    Panel1: TPanel;
    Timer1: TTimer;
    Memo2: TMemo;
    URLED: TEdit;
    SpeedButton1: TSpeedButton;
    ApplicationEvents1: TApplicationEvents;
    PopupMenu1: TPopupMenu;
    Restore1: TMenuItem;
    Minimize1: TMenuItem;
    quit1: TMenuItem;
    Restart1: TMenuItem;
    Chart1: TChart;
    Series1: TLineSeries;
    Series2: TLineSeries;
    Series3: TLineSeries;
    Series4: TLineSeries;
    chartbox: TCheckBox;
    procedure FormCreate(Sender: TObject);
    procedure SpeedButton1Click(Sender: TObject);
  private
    { Private declarations }
  protected
//  Procedure ControlWindow(Var Msg:TMessage); message WM_SYSCOMMAND;
//  Procedure IconMouse(var Msg:TMessage); message WM_USER+1;

  public
//    Procedure Ic(n:Integer;Icon:TIcon);
  end;
//Function setVariable(ObjName,VarName:widestring;value:string);
  TTCPHttpDaemon = class(TThread)
  private
    Sock:TTCPBlockSocket;
  public
    Constructor Create;
    Destructor Destroy; override;
    procedure Execute; override;
  end;

  TTCPHttpThrd = class(TThread)
  private
    Sock:TTCPBlockSocket;
  public
    Headers: TStringList;
    InputData, OutputData: TMemoryStream;
    Constructor Create (hsock:tSocket);
    Destructor Destroy; override;
    procedure Execute; override;
    function ProcessHttpRequest(Request, URI: string): integer;
  end;
  THardRec = packed record
     DateTimeSTR           :array[0..5] of ansichar;
     UpdateCounter         :int64;
     VersionSignature      :array[0..5] of ansichar;
     JSONAll : array[0..10000000] of ansichar;
  end;
  PHardRec = ^THardRec;
var
PrevUpdates :integer=0;
HardRec :phardrec;
testbuf : array[0..1000] of byte absolute hardrec;
shared : tsharedmem;
PortNum :integer = 9090;
textfromjson :string ='[]';
currentData :string = '{}';
testjson : string ='[{"time":"18:57:40","sbrkgu1":0,"sbrkgu2":0,"k1t6":272.73,"k1t12":295.05,"k1t13":288.41,"k1dt5t6":12.15,"k1dt3t4":2.73,"k1sbr":0,'+
                    '"k1vanna":0,"k1bo1":0.37,"k1bo2":0,"k2t6":108.89,"k2t12":211.58,"k2t13":286.86,"k2dt5t6":-2.02,"k2dt3t4":-1.91,"k2sbr":0,"k2vanna":0,'+
                    '"k2bo1":0,"k2bo2":58.79}]';

  starttime :double;
  HTTP: THTTPSend = nil;
  PrevUpdate : double = 0;
   HTTPsrv:TTCPHttpDaemon;
   HTTPSRVFORM:THTTPSRVFORM;
  URL : string;
  intsum : integer = 0;
  intcount: integer = 0;
  maxint : integer = 0;
  minint : integer = 10000;
  lastReq : double;
implementation

uses shellapi;
{$R *.dfm}
(*
procedure THTTPSRVForm.IconMouse(var Msg:TMessage);
Var p:tpoint;
begin
 GetCursorPos(p); // ���������� ���������� ������� ����
 Case Msg.LParam OF  // ��������� ����� ������ ���� ������
  WM_LBUTTONUP,WM_LBUTTONDBLCLK: {��������, ����������� �� ���������� ��� �������� ������ ����� ������ ���� �� ������. � ����� ������ ��� ������ ��������� ����������}
                   Begin
                    Ic(2,Application.Icon);  // ������� ������ �� ����
                    ShowWindow(Application.Handle,SW_SHOW); // ��������������� ������ ���������
                    ShowWindow(Handle,SW_SHOW); // ��������������� ���� ���������
                   End;
  WM_RBUTTONUP: {��������, ����������� �� ���������� ������ ������ ������ ����}
   Begin
    SetForegroundWindow(Handle);  // ��������������� ��������� � �������� ��������� ����
    PopupMenu1.Popup(p.X,p.Y);  // ���������� ������� ��� ����� TPopUp � ������� � ������� ���� ������
    PostMessage(Handle,WM_NULL,0,0);
   end;
 End;
end;

Procedure THTTPSRVForm.Ic(n:Integer;Icon:TIcon);
Var Nim:TNotifyIconData;
begin
 With Nim do
  Begin
   cbSize:=system.SizeOf(nim);
   Wnd:=Handle;
   uID:=1;
   uFlags:=NIF_ICON or NIF_MESSAGE or NIF_TIP;
   hicon:=Icon.Handle;
   uCallbackMessage:=wm_user+1;
   szTip:='WEB-Shell interface server';
  End;
 Case n OF
  1: Shell_NotifyIcon(Nim_Add,@Nim);
  2: Shell_NotifyIcon(Nim_Delete,@Nim);
  3: Shell_NotifyIcon(Nim_Modify,@Nim);
 End;
end;
Procedure THTTPSRVForm.ControlWindow(Var Msg:TMessage);
Begin
 IF Msg.WParam=SC_MINIMIZE then
  Begin
   Ic(1,Application.Icon);  // ????????? ?????? ? ????
   ShowWindow(Handle,SW_HIDE);  // ???????? ?????????
   ShowWindow(Application.Handle,SW_HIDE);  // ???????? ?????? ? TaskBar'?
 End else inherited;
End;
*)
procedure THTTPSRVForm.FormCreate(Sender: TObject);
var
 ff:tfilestream;
 str1 : string;
 objFileName:string;
 strlist : tstringlist;
begin
 startTime := now;
 startTime := now;
 while (now - StartTime)*24*3600 <3 do application.ProcessMessages;

 HTTPsrv:=TTCPHttpDaemon.create;
  lastReq := -1;
  timer1.OnTimer(self);
end;

Constructor TTCPHttpDaemon.Create;
begin
  inherited create(false);
  sock:=TTCPBlockSocket.create;
  FreeOnTerminate:=true;
  Priority:=tpNormal;
end;

Destructor TTCPHttpDaemon.Destroy;
begin
  Sock.free;
  inherited Destroy;
end;

procedure TTCPHttpDaemon.Execute;
var
  ClientSock:TSocket;
begin
 writeTimeLog('open sock');
  with sock do
    begin
      CreateSocket;
      setLinger(true,10);
      bind('0.0.0.0',IntToStr(PortNum));
      listen;
      writeTimeLog('Listen sock');
      repeat
        if terminated then break;
        if canread(1000) then
          begin
            writeTimeLog('Client read sock');
            ClientSock:=accept;
            if lastError=0 then TTCPHttpThrd.create(ClientSock);
          end;
      until false;
    end;
end;

{ TTCPHttpThrd }

Constructor TTCPHttpThrd.Create(Hsock:TSocket);
begin
  writeTimeLog('TCPHttpThrd.Create');

  inherited create(false);
  sock:=TTCPBlockSocket.create;
  Headers := TStringList.Create;
  InputData := TMemoryStream.Create;
  OutputData := TMemoryStream.Create;
  Sock.socket:=HSock;
  FreeOnTerminate:=true;
  Priority:=tpNormal;
end;

Destructor TTCPHttpThrd.Destroy;
begin
  Sock.free;
  Headers.Free;
  InputData.Free;
  OutputData.Free;
  inherited Destroy;
end;

procedure TTCPHttpThrd.Execute;
var
  b: byte;
  timeout: integer;
  s: string;
  method, uri, protocol: string;
  size: integer;
  x, n: integer;
  resultcode: integer;
begin
  timeout := 120000;
  //read request line
  s := sock.RecvString(timeout);
  if sock.lasterror <> 0 then
    Exit;
  if s = '' then
    Exit;
  method := fetch(s, ' ');
  if (s = '') or (method = '') then
    Exit;
  uri := fetch(s, ' ');
  if uri = '' then
    Exit;
  protocol := fetch(s, ' ');
  headers.Clear;
  size := -1;
  //read request headers
  if protocol <> '' then
  begin
    if pos('HTTP/', protocol) <> 1 then
      Exit;
    repeat
      s := sock.RecvString(Timeout);
      if sock.lasterror <> 0 then
        Exit;
      if s <> '' then
        Headers.add(s);
      if Pos('CONTENT-LENGTH:', Uppercase(s)) = 1 then
        Size := StrToIntDef(SeparateRight(s, ' '), -1);
    until s = '';
  end;
  //recv document...
  InputData.Clear;
  if size >= 0 then
  begin
    InputData.SetSize(Size);
    x := Sock.RecvBufferEx(InputData.Memory, Size, Timeout);
    InputData.SetSize(x);
    if sock.lasterror <> 0 then
      Exit;
  end;
  OutputData.Clear;
  ResultCode := ProcessHttpRequest(method, uri);
  sock.SendString('HTTP/1.0 ' + IntTostr(ResultCode) + CRLF);
  if protocol <> '' then
  begin
    headers.Add('Content-length: ' + IntTostr(OutputData.Size));
    headers.Add('Connection: close');
    headers.Add('Date: ' + Rfc822DateTime(now));
    headers.Add('Server: Synapse HTTP server demo');
    headers.Add('');
    for n := 0 to headers.count - 1 do
      sock.sendstring(headers[n] + CRLF);
  end;
  if sock.lasterror <> 0 then   Exit;
  Sock.SendBuffer(OutputData.Memory, OutputData.Size);
  if lastreq>0 then begin
    intsum := intsum+trunc((now-lastreq)*24*3600*1000);
    inc(intcount);
    if (now-lastreq)*24*3600*1000 >maxint then maxint := trunc((now-lastreq)*24*3600*1000);
    if (now-lastreq)*24*3600*1000 <minint then minint := trunc((now-lastreq)*24*3600*1000);
  end;
  lastReq := now;
  sock.CloseSocket;
end;

function TTCPHttpThrd.ProcessHttpRequest(Request, URI: string): integer;
var
  l: TStringlist;
  resp : ansistring;
  stmp,jreq :string;
  amppos:integer;
begin
//sample of precessing HTTP request:
// InputData is uploaded document, headers is stringlist with request headers.
// Request is type of request and URI is URI of request
// OutputData is document with reply, headers is stringlist with reply headers.
// Result is result code
  result := 504;
  if request = 'GET' then
  begin
    headers.Clear;
    headers.Add('Content-type: Text/Html');
    l := TStringList.Create;
    try
      if (pos('callback=',uri) <>0)  then begin
        stmp:=copy(uri,pos('callback=',uri)+9,length(uri));
        amppos:=pos('get_member',stmp);
        if amppos>0 then jreq:=copy(stmp,1,amppos-2);
      end;
      resp:=hardrec.JSONAll;
      resp:=jreq+'('+resp+');';
      l.Add(resp);
      l.SaveToStream(OutputData);
    finally
      l.free;
    end;
    Result := 200;
  end;
end;


procedure THTTPSRVForm.SpeedButton1Click(Sender: TObject);
var
  jtype :string;
  jsonstr:string;
  i, id :integer;
  r1,r2 :double;
//  rl : tstringlist;
  offset, position, h , g: integer;
  s:string;
  ff :tfilestream;
  r : array [0..255] of string;
  pointpos: integer;
  resrecord :string;
   FullProgPath: PwideChar;
   str22 : string;
Procedure SliceSeries(chart:tchart;maxlen : integer);
 var
  ic : integer;

begin
  for ic := 0 to chart.SeriesCount-1 do begin
    while chart.Series[ic].Count>maxlen do chart.Series[ic].Delete(0);
  end;
end;

begin
 caption :=formatDateTime('dd/mm/yyyy HH:NN:SS',now)+formatDateTime(' �����:dd/mm/yyyy HH:NN:SS',startTime);
 timer1.Enabled:=false;
 textfromJson:=hardrec.JSONall;
// memo2.Lines.Clear;
// memo2.Text:=textfromJson;
 if chartbox.Checked then begin
   if Lastreq>0 then begin
     if intcount>0 then begin
      if chartbox.Checked then  series3.AddXY(now,intsum/intcount);
     end;
     if chartbox.Checked then  series4.AddXY(now,hardrec.UpdateCounter-prevUpdates);
     if chartbox.Checked then series1.AddXY(now,minint);
     if chartbox.Checked then series2.AddXY(now,maxint);

   end;
   SliceSeries(chart1,1000);
 end;
 PrevUpdates := hardrec.UpdateCounter;
 intsum := 0;
 intCount:=0;
 minInt :=1000;
 maxInt:=0;
 timer1.Enabled:=true;
end;

var
 jcount :integer;
 str :string;

var
ini :tinifile;
initialization
   shared := tsharedmem.Create('webredis tempore mutanur',10000000);
   HardRec:=Pointer(Integer(shared.Buffer)+100);
   hardRec.UpdateCounter := 0;
   LastReq := now;
end.
