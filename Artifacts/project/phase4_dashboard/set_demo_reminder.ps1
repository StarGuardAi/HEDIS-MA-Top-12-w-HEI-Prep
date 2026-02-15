# One-time reminder: Saturday at noon - StarGuard AI Demo Polish
$today = Get-Date
$daysUntilSaturday = [int][DayOfWeek]::Saturday - [int]$today.DayOfWeek
if ($daysUntilSaturday -le 0) { $daysUntilSaturday += 7 }
$saturdayNoon = $today.AddDays($daysUntilSaturday).Date.AddHours(12)
$trigger = New-ScheduledTaskTrigger -Once -At $saturdayNoon
$action = New-ScheduledTaskAction -Execute "msg" -Argument "$env:USERNAME 'Time to work on StarGuard AI Demo Polish (Option A)!'"
Register-ScheduledTask -TaskName "StarGuardDemoReminder" -Trigger $trigger -Action $action
Write-Host "Reminder set for $($saturdayNoon.ToString('yyyy-MM-dd HH:mm'))"
