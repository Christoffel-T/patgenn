#Requires AutoHotkey v2.0
win := "Exchange - Google Chrome"
loop {
	if !WinExist(win)
	{
		continue
	}
	x := random(0, 15)
	y := random(0, 30)
	try {
		WinActivate win
	}
	Sleep y*10
	MouseMove 480-x, 403+y, 10
	Sleep x*10
	MouseMove 482-x, 453+y, 10
	Sleep y*500
}
Return

$esc::
{
	ExitApp
}
$+esc::
{
	Pause -1
}