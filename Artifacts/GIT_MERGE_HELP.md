# Git Merge Commit Help

## Current Situation
You're in a git merge commit message editor (likely vim/vi). You need to save and exit to complete the merge.

## Quick Exit (Accept Default Message)

### If in Vim/Vi:
1. Press `Esc` (to ensure you're in command mode)
2. Type `:wq` (write and quit)
3. Press `Enter`

Or simply:
- Press `Esc`
- Type `:x` (save and exit)
- Press `Enter`

### If in Nano:
- Press `Ctrl + X` (exit)
- Press `Y` (yes, save)
- Press `Enter`

## Alternative: Skip Editor
If you want to avoid the editor next time, you can set a default merge message:
```powershell
git pull origin main --no-rebase --no-edit
```

## After Exiting Editor
Once you save and exit:
1. The merge will complete
2. Then you can push: `git push origin main`

