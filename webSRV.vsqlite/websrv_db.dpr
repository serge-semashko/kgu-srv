program websrv_db;

uses
  Forms,
  uwebserv in 'uwebserv.pas' {HTTPSRVForm},
  uLkJSON in 'UlkJSON.pas';

{$R *.res}

begin
//ddddd
  Application.Initialize;
  Application.CreateForm(THTTPSRVForm, HTTPSRVForm);
  Application.Run;
end.
