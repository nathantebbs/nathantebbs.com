+++
title = "Migrating from Neovim to Emacs"
date = 2025-09-17T00:00:00-07:00
tags = ["Emacs", "Configuration"]
draft = false
summary = "A reflection on moving from a complex Neovim setup to a simpler, more intentional Emacs configuration that balances customization with minimalism."
+++

<div class="ox-hugo-toc toc">

<div class="heading">Table of Contents</div>

- [Quick link(s):](#quick-link--s)
- [Background](#background)
    - [Discovering Alternatives](#discovering-alternatives)
    - [Return to Minimalsim](#return-to-minimalsim)
- [Emacs Configuration](#emacs-configuration)
    - [Basic U/I + Basic Options](#basic-u-i-plus-basic-options)
    - [Fixing Directory Clutter](#fixing-directory-clutter)
    - [Keybindings](#keybindings)
    - [Custom Functionality](#custom-functionality)
    - [Package Setup](#package-setup)
    - [Installing packages via 'use-package'](#installing-packages-via-use-package)
    - [Theme](#theme)
- [Sources](#sources)

</div>
<!--endtoc-->

<div class="image-stack">
    <img src="/images/lazyvim1.png" alt="Lazy Neovim Distrobution">
    <img src="/images/doom1.png" alt="Doom Emacs Distrobution">
</div>


## Quick link(s): {#quick-link--s}

-   [.emacs](https://raw.githubusercontent.com/nathantebbs/dotfiles/refs/heads/main/.emacs)
-   [nvim/](https://github.com/nathantebbs/dotfiles/tree/main/nvim)


## Background {#background}

Since starting my journey into discovering different development environments within my personal linux setup,
attempting to make them practical either for Computer Science school work or just personal projects has proven
an effecient procrastination technique. However, I love text editors, and the feeling of customizing a Neovim plugin for
the first time is wonderful. However, the ecosystem surround Neovim and the pace at which the plugins evolve I quickly became
exausted trying to keep up after being out of touch with the editor for times.


### Discovering Alternatives {#discovering-alternatives}

Around late last year I discovered Emacs, first because of [org-mode](https://www.orgmode.org), then later falling in love with the GUI editor first PDE, and [evil-mode](https://github.com/emacs-evil/evil).

I started out using an out-of-the-box distrobution of evil-mode Emacs called [doom-emacs](https://github.com/doomemacs/doomemacs). Doom provided a way to keep the lovely
vim keybinds that have been baked into my brain while allowing me to use cool native Emacs features and plugins.

Over time, the utility for me to use Neovim for text editing has shifted mainly to not provide IDE features. I was inspired
by trying to edit some assignment code that I had secure copied into my univerities virtual machine. For fun, I decided
to clone my Neovim config and benefit from the LSP setup. However, after long download times and heavy lag I realized that I had
entirely defeated the purpose of my light-weight text editor by giving it the resposibility of a full blown IDE.

That said, Neovim has amazing stock featuers, and in the nightly branch now has a built-in package manager. Which you can see
in my Neovim config's [init.lua](https://github.com/nathantebbs/dotfiles/blob/main/nvim/init.lua#L17)


### Return to Minimalsim {#return-to-minimalsim}

After getting familiar with doom, I realized that I was loading 200 packages on startup, and I couldn't even tell you what half of
them were. Also, doom comes with a lot of custom Emacs keybindings, and I love evil mode but trying remap all baseline functionality
breaks the reason why you choose an editor to. Basically, I don't want to turn Emacs into Neovim, I just want hjkl.


## Emacs Configuration {#emacs-configuration}


### Basic U/I + Basic Options {#basic-u-i-plus-basic-options}

When you first start Emacs, there are a lot of simple U/I options that should be off by default
for any competant user. Below we remove clunky things like window decorations, enable line numbers, autopairs, which-key
org-agenda files, &lt;C-u&gt; for up scroll, and no more annoying backup~ files.

```elisp
;; Remove window decorations
(menu-bar-mode -1)
(tool-bar-mode -1)
(scroll-bar-mode -1)

;; Lines
(global-display-line-numbers-mode t)
(setq truncate-lines t) ;; No visual wrapping

(setq inhibit-startup-screen t) ;; Disable startup screen

;; Tabs
(setq-default indent-tabs-mode nil)
(setq-default tab-width 2)

;; Mini-buffer completion mode
(fido-vertical-mode)

;; Misc
(electric-pair-mode t) ;; Autopairs
(which-key-mode) ;; which-key
```


### Fixing Directory Clutter {#fixing-directory-clutter}

In Emacs, by default, autosave and backup versions of a file that you are editing
may be saved in the current working directory. This usually results in errors, and just
overall messiness in projects. To fix this, and customize a couple more options we are going
to define, create, and use directories in the user-emacs-directory (usually ~/.emacs.d)

```elisp

;; Create backup and autosave directories if they don't exist
(let ((backup-dir (expand-file-name "backups/" user-emacs-directory))
      (autosave-dir (expand-file-name "autosaves/" user-emacs-directory)))
  (make-directory backup-dir t)
  (make-directory autosave-dir t)

  ;; Backups (files ending with ~)
  (setq backup-directory-alist `(("." . ,backup-dir))
        make-backup-files t
        version-control t          ; use versioned backups
        kept-new-versions 10
        kept-old-versions 2
        delete-old-versions t)

  ;; Autosave files (#foo#)
  (setq auto-save-file-name-transforms `((".*" ,autosave-dir t))
        auto-save-default t
        auto-save-timeout 20        ; save every 20 sec idle
        auto-save-interval 200))    ; or every 200 keystrokes
```


### Keybindings {#keybindings}

In my configuration, I do most of my keybinding within the relative use-package block. If you would like to define
global maps outside of use-package, make sure the package is loaded before setting any options or keybindings.
If you want to see an example of defining keybindings within the use-package block, then refer to the evil-mode [configuration](#evil-mode-configuration)
after we bootstrap our package installation system.

```elisp
;; Example global definition
(global-set-key (kbd "C-x C-b") 'ibuffer)

;; Example package specific definition
(with-eval-after-load 'dired
  (define-key dired-mode-map (kbd "-") #'dired-up-directory))
```


### Custom Functionality {#custom-functionality}

It may also be useful to define custom functions to be triggered either on a keybinding
or just activated through M-x. One of the most useful functions I have included in my configuration
is for connecting to a commonly used ssh host through dired.

```elisp
(defun connect-lectura ()
  (interactive)
  (dired "/ssh:ntebbs@lec.cs.arizona.edu:/home/ntebbs/"))
```


### Package Setup {#package-setup}

This is the basic bootstrap for straight.el which we will use to install external packages below.

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


### Installing packages via 'use-package' {#installing-packages-via-use-package}

Most of the packages you install are up to personal preference and goals with your own config. However,
I have decided to include my work in progress evil-mode configuration, but the principles of
use-package stay almost the same for any package.


#### Evil Mode Configuration {#evil-mode-configuration}

```elisp
;; NOTE: This line must after the bootstrap but before 'use-package' uses
(straight-use-package 'use-package)
;; Evil mode
(use-package evil
  :straight t

  :init
  (setq evil-want-C-u-scroll t) ;; Fixes C-u scrolling

  :config
  (evil-mode 1)

  ;; =================
  ;; *Evil* Keymaps
  ;; =================

  ;; Leader
  (define-prefix-command 'nate/leader-map)
  (define-key evil-normal-state-map (kbd "SPC") 'nate/leader-map)
  (define-key evil-visual-state-map (kbd "SPC") 'nate/leader-map)

  ;; Finding Files
  (define-key nate/leader-map (kbd "s n") (lambda () (interactive) (fzf-find-file-in-dir "~/dotfiles/")))
  (define-key nate/leader-map (kbd "s f") (lambda () (interactive) (fzf-find-file)))
  (define-key nate/leader-map (kbd "s p") (lambda () (interactive) (fzf-find-file-in-dir "~/dev/probe/")))
  (define-key nate/leader-map (kbd "f") #'find-file)
  (define-key nate/leader-map (kbd "e") #'dired-jump)

  ;; Magit
  (define-key nate/leader-map (kbd "g s") #'magit)

  ;; Org Mode
  (define-key nate/leader-map (kbd "o p") #'org-pomodoro)
  (define-key nate/leader-map (kbd "o a") #'org-agenda)
  (define-key nate/leader-map (kbd "o c") #'org-capture)
  (define-key nate/leader-map (kbd "o v") #'org-tags-view)
  (define-key nate/leader-map (kbd "o t") (lambda () (interactive) (find-file "~/org/todo.org")))
  (define-key nate/leader-map (kbd "o n") (lambda () (interactive) (find-file "~/org/notes.org")))
  (define-key nate/leader-map (kbd "o P") (lambda () (interactive) (find-file "~/org/projects.org")))
  (define-key nate/leader-map (kbd "o A") (lambda () (interactive) (find-file "~/org/assignments.org")))

  ;; State
  (define-key evil-insert-state-map (kbd "C-g") 'evil-change-to-previous-state)
  (define-key evil-visual-state-map (kbd "C-g") 'evil-change-to-previous-state)

  ;; Buffers
  (define-key nate/leader-map (kbd "b b") #'switch-to-buffer)
  (define-key nate/leader-map (kbd "b i") #'ibuffer-other-window)
  (define-key nate/leader-map (kbd "b k") #'kill-buffer)

  ;; Config
  (define-key nate/leader-map (kbd "r r") (lambda () (interactive) (load-file "~/.emacs"))))
```


### Theme {#theme}

I have chosen to use an external theme as apposed to a built in themes. The main reasoning I have behind this is because
my emacs config is designed to be lightweight but not portable, that is I won't be installing this on any VMs.

```elisp
;; Simple Option
;; use M-x describe-theme RET to see available themes
(load-theme 'modus-vivendi)

;; Current Approach (using straight.el)
(use-package gruber-darker-theme
  :straight t
  :config
  (load-theme 'gruber-darker t))
```

<img src="/images/emacs.png" alt="Final product of config in action with the colorscheme set">


## Sources {#sources}

-   [Loose Leaf Learning (YT)](https://www.youtube.com/@LooseLeafLearning)
-   [Gruber Darker (Theme)](https://github.com/rexim/gruber-darker-theme)
-   [evil-mode](https://github.com/emacs-evil/evil)
-   [straight.el (Package Manager)](https://github.com/radian-software/straight.el)
-   [Doom Emacs (IDE Alternative)](https://github.com/doomemacs/doomemacs)
