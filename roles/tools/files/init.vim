set termguicolors
color simple-dark

autocmd FileType yaml setlocal ts=2 sts=2 sw=2 expandtab indentkeys-=0#
au BufNewFile,BufReadPost * if &filetype == "yaml" | set softtabstop=2 | set indentkeys-=0# | endif

let g:syntastic_yaml_checkers = ['yamllint']

autocmd Filetype make setlocal ts=4 sts=4 sw=4
autocmd FileType groovy setlocal et
let g:netrw_banner = 0
let g:netrw_liststyle = 0
"let g:netrw_browse_split = 2
let g:netrw_altv = 1
let g:netrw_winsize = 10
"augroup ProjectDrawer
"  autocmd!
"  autocmd VimEnter * :Vexplore | wincmd w
"augroup END
