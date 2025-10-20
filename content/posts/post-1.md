+++
title = "Migrating from Neovim to Emacs"
date = 2025-09-17T00:00:00-07:00
draft = false
+++

<div class="ox-hugo-toc toc">

<div class="heading">Table of Contents</div>

- [Background](#background)
- [Emacs Configuration](#emacs-configuration)
    - [Basic U/I + Basic Options](#basic-u-i-plus-basic-options)
    - [Keybindings](#keybindings)
    - [Package Setup](#package-setup)

</div>
<!--endtoc-->

<div class="image-stack">
    <img src="/images/lazyvim1.png" alt="Lazy Neovim Distrobution">
    <img src="/images/doom1.png" alt="Doom Emacs Distrobution">
</div>


## Background {#background}

Since starting my journey into discovering different development environments within my personal linux setup,
and attempting to make them practical either for Computer Science school work or just personal projects has proven
an effecient procrastination technique. However, I love text editors, and the feeling of customizing a neovim plugin for
the first time is wonderful. However, the ecosystem surround neovim and the pace at which the plugins evolve I quickly became
exausted trying to keep up after being out of touch with the editor for times. Around late last year I discovered Emacs, first
because of [org-mode](https://www.orgmode.org), then later falling in love with the GUI editor first PDE, and [evil-mode](https://github.com/emacs-evil/evil).

I started out using an out-of-the-box distrobution of evil-mode Emacs called [doom-emacs](https://github.com/doomemacs/doomemacs). Doom provided a way to keep the lovely
vim keybinds that have been baked into my brain while allowing me to use cool native Emacs features and plugins. Additionally,
the utility for me to use neovim for text editing has shifted mainly to not provide IDE features. This was inspired by trying to
edit some assignment code that I had secure copied into my univerities virtual machine. For fun, I decided to clone my neovim config
and benefit from the LSP setup. However, after long download times and heavy lag I realized that I had entirely defeated the purpose
of my light-weight text editor by giving it the resposibility of a full blown IDE. Furthermore, neovim has amazing stock featuers,
and in the nightly branch now has a built-in package manager, which is quite intriguing.

After getting familiar with doom, I realized that I was loading 200 packages on startup, and I couldn't even tell you what half of
them were. Also, doom comes with a lot of custom Emacs keybindings, and I love evil mode but trying remap all baseline functionality
breaks the reason why you choose an editor to. Basically, I don't want to turn Emacs into Neo-vim, I just want hjkl.


## Emacs Configuration {#emacs-configuration}


### Basic U/I + Basic Options {#basic-u-i-plus-basic-options}

```elisp
;; Remove window decorations
(menu-bar-mode -1)
(tool-bar-mode -1)
(scroll-bar-mode -1)

(global-display-line-numbers-mode t) ;; Line numbers

(setq inhibit-startup-screen t) ;; Disable startup screen

;; Tabs
(setq-default indent-tabs-mode nil)
(setq-default tab-width 2)

;; Mini-buffer completion mode
(fido-vertical-mode)

;; Misc
(electric-pair-mode t) ;; Autopairs
(which-key-mode) ;; which-key
(setq org-agenda-files '("~/org/todo.org"))
(setq evil-want-C-u-scroll t) ;; Please fix scroll!! (this works)

;; Change file backup location
(setq make-backup-file nil) ;; No more
(setq auto-save-default nil) ;; No autosave files
(setq backup-directory-alist '((".*" . "~/.Trash")))
```

When you first start Emacs, there are a lot of simple U/I options that should be off by default
for any competant user. Below we remove clunky things like window decorations, enable line numbers, autopairs, which-key
org-agenda files, &lt;C-u&gt; for up scroll, and no more annoying backup~ files.


### Keybindings {#keybindings}

```elisp

;; ===============
;; Keybindings
;; ===============

(global-set-key (kbd "C-x C-b") 'ibuffer)
(global-set-key (kbd "C-x C-c") '(lambda () (interactive) (find-file "~/.emacs")))
(global-set-key (kbd "C-x e") 'eval-buffer)
(global-set-key (kbd "C-c a") 'org-agenda-list)
(global-set-key (kbd "C-c o") '(lambda () (interactive) (find-file "~/org/todo.org")))
```


### Package Setup {#package-setup}


#### Bootstrapping straight.el {#bootstrapping-straight-dot-el}

```elisp

;; Straight.el bootstrap
(defvar bootstrap-version)
(let ((bootstrap-file
       (expand-file-name
        "straight/repos/straight.el/bootstrap.el"
        (or (bound-and-true-p straight-base-dir)
            user-emacs-directory)))
      (bootstrap-version 7))
  (unless (file-exists-p bootstrap-file)
    (with-current-buffer
        (url-retrieve-synchronously
         "https://raw.githubusercontent.com/radian-software/straight.el/develop/install.el"
         'silent 'inhibit-cookies)
      (goto-char (point-max))
      (eval-print-last-sexp)))
  (load bootstrap-file nil 'nomessage))
```


#### Installing packages via 'use-package' {#installing-packages-via-use-package}

```elisp

;; ===============
;; Install Packages:
;; ===============

(straight-use-package 'use-package)

;; Theme
(use-package gruber-darker-theme
  :straight t
  :config
  (load-theme 'gruber-darker t))

;; Evil mode
(use-package evil
  :straight t)
(require 'evil)
(evil-mode 1)

;; Magit
(use-package magit
  :straight t)

;; Devdocs
;; NOTE: use M-x devdocs-install
(use-package devdocs
  :straight t)

;; Company
(use-package company
  :straight t
  :hook (prog-mode . global-company-mode))

;; Fzf
(use-package fzf
  :bind ("C-c s" . fzf-grep)
  :straight t)


;; Markdown
(use-package markdown-mode
  :straight t
  :mode ("\\.md\\'" . markdown-mode)
  :init
  (setq markdown-command "multimarkdown")  ;; or "pandoc"
  :config
  (setq markdown-fontify-code-blocks-natively t))

;; ox-hugo
(use-package ox-hugo
  :straight t
  :after ox)
```
