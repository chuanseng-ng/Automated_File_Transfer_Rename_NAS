# Define the source directory where the files are located
$sourceDirectory = "E:\Torrented Files"

# Change directory to the source directory
Set-Location -Path $sourceDirectory

# Get all MKV files in the source directory
$files = Get-ChildItem -Path $sourceDirectory -File | Where-Object { $_.Extension -eq ".mkv" }

# Echo initial message
Write-Host "Found $($files.Count) MKV files to process."

# Iterate through each file
foreach ($file in $files) {
    # Echo progress message
    Write-Host "Processing file: $($file.FullName)"
	
    # Extract the file name without extension
    $fileName = $file.BaseName

    # Extract the pattern between "]" and "-"
    $pattern = $fileName -replace '^.*?\] ', '' -replace ' - [0-9].*$'
	# Further extract season name if exist
	if ($pattern -match 'S[0-9]') {
		$pattern = $fileName -replace '^.*?\] ', '' -replace ' S[0-9].*$'
	}
	
    # Define the destination directory based on the pattern
    $destinationDirectory = "Z:\Animes\$pattern"

    # Check if the destination directory exists, if not, report it
    if (-not (Test-Path $destinationDirectory)) {
        $missingDestinations += "$pattern`n"
        Write-Host "Destination directory does not exist: $pattern"
    } else {
        Write-Host "Destination directory exists: $destinationDirectory"
		# Check if sub-folder exists
		$subFolders = Get-ChildItem -Path $destinationDirectory -Directory
		if ($subFolders.Count -eq 0) {
			# Move the file into the main folder
			Move-Item -LiteralPath "$($file.FullName)" -Destination "$destinationDirectory"
			Write-Host "Moved file - $file - to main folder: $destinationDirectory"
		} else {
			# Determine the highest season number
			$highestSeason = ($subFolders | Where-Object { $_.Name -match 'Season (\d+)' } | ForEach-Object { [int]$matches[1] } | Measure-Object -Maximum).Maximum

			# Update the destination directory with the highest season number
			$destinationDirectory = Join-Path -Path $destinationDirectory -ChildPath "Season $highestSeason"

			# Move the file to the sub-folder with the highest season number
			Move-Item -LiteralPath "$($file.FullName)" -Destination "$destinationDirectory"
			Write-Host "Moved file - $file - to sub-folder: $destinationDirectory"
		}
	}

    # Move the file to the destination directory
    #Move-Item -Path $file -Destination $destinationDirectory
    #Write-Host "Moved file to: $destinationDirectory"
}

# Report missing destination directories if any
if ($missingDestinations.Count -gt 0) {
    Write-Host "Missing destination directories:"
    $missingDestinations | ForEach-Object { Write-Host $_}
	Write-Host "Check above-mentioned files and do manual move"
} else {
	# Echo completion message
	Write-Host "All files processed."
}