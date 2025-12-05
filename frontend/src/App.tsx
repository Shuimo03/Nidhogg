import { useEffect, useState } from 'react'
import { Button, Card, CardBody, Chip } from '@heroui/react'
import { MessageSquare, Plus, Folder, FileText, Settings, SunMedium, Moon, Monitor } from 'lucide-react'

type ColorScheme = 'system' | 'light' | 'dark'

function useColorScheme() {
  const [scheme, setScheme] = useState<ColorScheme>(() => {
    if (typeof window === 'undefined') return 'system'
    const saved = window.localStorage.getItem('nidhogg.theme') as ColorScheme | null
    return saved ?? 'system'
  })
  const [isDark, setIsDark] = useState(true)

  useEffect(() => {
    if (typeof window === 'undefined') return
    const media = window.matchMedia('(prefers-color-scheme: dark)')

    const apply = () => {
      const dark = scheme === 'dark' || (scheme === 'system' && media.matches)
      setIsDark(dark)
      if (dark) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    }

    apply()

    const listener = () => {
      if (scheme === 'system') {
        apply()
      }
    }

    media.addEventListener('change', listener)
    return () => media.removeEventListener('change', listener)
  }, [scheme])

  useEffect(() => {
    if (typeof window === 'undefined') return
    if (scheme === 'system') {
      window.localStorage.removeItem('nidhogg.theme')
    } else {
      window.localStorage.setItem('nidhogg.theme', scheme)
    }
  }, [scheme])

  return { scheme, setScheme, isDark }
}

function App() {
  const { scheme, setScheme, isDark } = useColorScheme()

  const cycleScheme = () => {
    setScheme((prev) => {
      if (prev === 'system') return 'dark'
      if (prev === 'dark') return 'light'
      return 'system'
    })
  }

  const ThemeIcon = scheme === 'system' ? Monitor : scheme === 'dark' ? Moon : SunMedium

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-zinc-50 via-white to-zinc-50 text-zinc-900 dark:from-zinc-950 dark:via-zinc-900 dark:to-zinc-950 dark:text-zinc-100">
      {/* 左侧：会话列表 */}
      <aside className="w-64 border-r border-zinc-200 bg-zinc-50/80 backdrop-blur-sm p-5 dark:border-zinc-800/40 dark:bg-zinc-900/30">
        <div className="mb-6">
          <h2 className="text-xs font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-500">
            Sessions
          </h2>
        </div>
        <div className="space-y-3">
          <Card className="rounded-2xl border border-violet-500/20 bg-gradient-to-br from-violet-500/10 via-purple-500/5 to-transparent shadow-lg shadow-violet-500/5 dark:from-violet-500/10 dark:via-purple-500/5">
            <CardBody className="px-4 py-3.5">
              <div className="flex items-center gap-3">
                <div className="rounded-xl bg-gradient-to-br from-violet-500/20 to-purple-500/20 p-1.5 ring-1 ring-violet-500/30">
                  <MessageSquare className="h-4 w-4 text-violet-500 dark:text-violet-400" />
                </div>
                <span className="text-sm font-medium text-zinc-900 dark:text-zinc-100">Current MVP discussion</span>
              </div>
            </CardBody>
          </Card>
          <Button
            variant="flat"
            disableAnimation
            className="w-full justify-start rounded-xl border-0 bg-zinc-100 text-zinc-700 hover:bg-zinc-200 dark:bg-zinc-800/30 dark:text-zinc-300 dark:hover:bg-zinc-800/50"
            startContent={<Plus className="h-4 w-4" />}
          >
            New session
          </Button>
        </div>
      </aside>

      {/* 中间：对话区 */}
      <main className="flex flex-1 flex-col border-r border-zinc-200 dark:border-zinc-800/40">
        {/* Header */}
        <header className="flex items-center justify-between border-b border-zinc-200 bg-zinc-50/80 backdrop-blur-sm px-6 py-4 dark:border-zinc-800/40 dark:bg-zinc-900/40">
          <div className="flex items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-gradient-to-br from-violet-500 via-purple-500 to-fuchsia-500 shadow-lg shadow-violet-500/30">
              <span className="text-xs font-bold text-white">N</span>
            </div>
            <div>
              <h1 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Nidhogg</h1>
              <span className="text-xs text-zinc-500 dark:text-zinc-500">Chat</span>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <Chip
              variant="flat"
              size="sm"
              className="rounded-full bg-gradient-to-r from-violet-500/10 to-purple-500/10 text-zinc-700 border border-violet-500/20 shadow-sm dark:text-zinc-300 dark:border-violet-500/20"
            >
              <span className="text-xs">Token</span>
              <span className="ml-1.5 font-semibold text-violet-600 dark:text-violet-400">0 / 128k</span>
            </Chip>
            <Button
              isIconOnly
              variant="light"
              disableAnimation
              size="sm"
              className="min-w-8 h-8 rounded-lg text-zinc-600 hover:text-zinc-900 hover:bg-zinc-200 dark:text-zinc-400 dark:hover:text-zinc-200 dark:hover:bg-zinc-800/50"
              onPress={cycleScheme}
            >
              <ThemeIcon className="h-4 w-4" />
            </Button>
            <Button
              isIconOnly
              variant="light"
              disableAnimation
              size="sm"
              className="min-w-8 h-8 rounded-lg text-zinc-600 hover:text-zinc-900 hover:bg-zinc-200 dark:text-zinc-400 dark:hover:text-zinc-200 dark:hover:bg-zinc-800/50"
            >
              <Settings className="h-4 w-4" />
            </Button>
          </div>
        </header>

        {/* Chat Content */}
        <section className="flex-1 overflow-y-auto bg-white px-6 py-8 dark:bg-zinc-950/50">
          <div className="mx-auto max-w-3xl">
            <div className="flex items-center justify-center py-16">
              <div className="rounded-2xl bg-zinc-100/80 p-6 border border-zinc-200 backdrop-blur-sm dark:bg-zinc-900/40 dark:border-zinc-800/40">
                <p className="text-sm text-zinc-600 dark:text-zinc-400">
                  对话内容区域（后续接入模型与 chats/*.md 持久化）。
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Input Footer */}
        <footer className="border-t border-zinc-200 bg-zinc-50/80 backdrop-blur-sm p-5 dark:border-zinc-800/40 dark:bg-zinc-900/40">
          <div className="mx-auto max-w-3xl">
            <Card className="rounded-2xl border border-violet-500/20 bg-gradient-to-br from-zinc-100/80 via-zinc-50/60 to-zinc-100/80 shadow-xl shadow-violet-500/5 dark:from-zinc-900/80 dark:via-zinc-800/60 dark:to-zinc-900/80">
              <CardBody className="p-4">
                <div className="flex items-end gap-2.5">
                  <textarea
                    placeholder="和 Nidhogg 聊聊你的 PRD、space 或代码想法…"
                    className="flex-1 resize-none rounded-lg border border-zinc-300 bg-white px-4 py-2.5 text-sm text-zinc-900 placeholder:text-zinc-400 focus:border-violet-500/40 focus:bg-white focus:outline-none focus:ring-1 focus:ring-violet-500/20 transition-all dark:border-zinc-700/50 dark:bg-zinc-900/60 dark:text-zinc-100 dark:placeholder:text-zinc-500 dark:focus:bg-zinc-900/80"
                    rows={2}
                  />
                  <Button
                    color="primary"
                    disableAnimation
                    className="h-[42px] rounded-lg bg-gradient-to-r from-violet-500 to-purple-500 px-5 font-medium text-white shadow-md shadow-violet-500/20 hover:from-violet-600 hover:to-purple-600"
                    endContent={<MessageSquare className="h-4 w-4" />}
                  >
                    Send
                  </Button>
                </div>
              </CardBody>
            </Card>
          </div>
        </footer>
      </main>

      {/* 右侧：文件树 */}
      <aside className="w-80 bg-zinc-50/80 backdrop-blur-sm p-5 dark:bg-zinc-900/30">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-xs font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-500">
            Project
          </h2>
          <Button
            size="sm"
            variant="flat"
            disableAnimation
            className="h-7 rounded-lg border-0 bg-zinc-100 text-xs text-zinc-700 hover:bg-zinc-200 dark:bg-zinc-800/30 dark:text-zinc-300 dark:hover:bg-zinc-800/50"
          >
            Select…
          </Button>
        </div>

        <div className="space-y-3">
          <Card className="rounded-2xl border border-amber-500/20 bg-gradient-to-br from-amber-500/10 via-orange-500/5 to-transparent shadow-lg shadow-amber-500/5">
            <CardBody className="px-4 py-3.5">
              <div className="flex items-center gap-2.5">
                <div className="rounded-lg bg-gradient-to-br from-amber-500/20 to-orange-500/20 p-1.5 ring-1 ring-amber-500/30">
                  <Folder className="h-4 w-4 text-amber-500 dark:text-amber-400" />
                </div>
                <span className="text-xs font-semibold text-zinc-900 dark:text-zinc-100">prd/</span>
              </div>
              <div className="mt-2.5 flex items-center gap-2 pl-7">
                <div className="rounded-md bg-gradient-to-br from-emerald-500/20 to-teal-500/20 p-1 ring-1 ring-emerald-500/30">
                  <FileText className="h-3 w-3 text-emerald-500 dark:text-emerald-400" />
                </div>
                <span className="text-xs text-zinc-600 dark:text-zinc-400">mvp-design.md</span>
              </div>
            </CardBody>
          </Card>

          <Card className="rounded-2xl border border-cyan-500/20 bg-gradient-to-br from-cyan-500/10 via-blue-500/5 to-transparent shadow-lg shadow-cyan-500/5">
            <CardBody className="px-4 py-3.5">
              <div className="flex items-center gap-2.5">
                <div className="rounded-lg bg-gradient-to-br from-cyan-500/20 to-blue-500/20 p-1.5 ring-1 ring-cyan-500/30">
                  <Folder className="h-4 w-4 text-cyan-500 dark:text-cyan-400" />
                </div>
                <span className="text-xs font-semibold text-zinc-900 dark:text-zinc-100">space/</span>
              </div>
              <div className="mt-2.5 flex items-center gap-2 pl-7">
                <div className="rounded-md bg-gradient-to-br from-emerald-500/20 to-teal-500/20 p-1 ring-1 ring-emerald-500/30">
                  <FileText className="h-3 w-3 text-emerald-500 dark:text-emerald-400" />
                </div>
                <span className="text-xs text-zinc-600 dark:text-zinc-400">notes.md</span>
              </div>
            </CardBody>
          </Card>
        </div>
      </aside>
    </div>
  )
}

export default App
