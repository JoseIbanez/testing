function no-floppy {
param ($name)
$floppy = Get-FloppyDrive -VM $name
Set-FloppyDrive -Floppy $floppy -NoMedia:$true -confirm:$false
}
