import {
  defineComponent,
  computed,
  type VNode,
  onMounted,
  nextTick,
  ref,
  watch,
} from "vue";
import { marked, type Tokens } from "marked";
import markedKatex from "marked-katex-extension";
import DOMPurify from "dompurify";
import mermaid from "mermaid";
import {
  NH1,
  NH2,
  NH3,
  NH4,
  NH5,
  NH6,
  NA,
  NP,
  NOl,
  NUl,
  NLi,
  NCode,
  NText,
  NTable,
  NImage,
  NDivider,
  NBlockquote,
  NEquation,
} from "naive-ui";

marked.use(markedKatex({ throwOnError: false }));

export default defineComponent({
  name: "MarkdownRender",
  props: {
    content: {
      type: String,
      required: true,
      default: "",
    },
  },
  setup(props) {
    // Mermaid initialization
    onMounted(() => {
      mermaid.initialize({
        startOnLoad: false,
        theme: "dark",
        securityLevel: "loose",
        logLevel: 5, // 禁用错误日志
      });
      renderMermaid();
    });

    const renderMermaid = async () => {
      await nextTick();
      const nodes = document.querySelectorAll(".mermaid-diagram");

      // 并发渲染以提高速度
      await Promise.all(
        Array.from(nodes).map(async (node) => {
          if (node.querySelector("svg") || node.getAttribute("data-processed"))
            return;

          const content = node.textContent || "";
          const cleanContent = content.trim();
          if (!cleanContent) return;

          // 标记正在处理，防止重复
          node.setAttribute("data-processed", "true");

          const id = `mermaid-${Math.random().toString(36).substr(2, 9)}`;
          try {
            const { svg } = await mermaid.render(id, cleanContent);
            node.innerHTML = svg;
          } catch (error) {
            console.error("Mermaid rendering failed:", error);
            node.innerHTML = `<pre style="color: #ff6b6b; background: #2d2d2d; padding: 12px; border-radius: 4px; overflow: auto; white-space: pre-wrap;">Mermaid Error:\n${(error as any).message || error}</pre>`;
          }
        }),
      );
    };

    const tokens = computed(() => {
      if (!props.content) return [];
      return marked.lexer(props.content);
    });

    watch(
      () => props.content,
      () => {
        renderMermaid();
      },
    );

    const renderInline = (inlineTokens?: Tokens.Generic[]): any[] => {
      if (!inlineTokens) return [];

      return inlineTokens.map((token, index) => {
        const key = index;
        switch (token.type) {
          case "text":
            return token.text;
          case "strong":
            return <strong key={key}>{renderInline(token.tokens)}</strong>;
          case "em":
            return <em key={key}>{renderInline(token.tokens)}</em>;
          case "del":
            return <del key={key}>{renderInline(token.tokens)}</del>;
          case "codespan":
            return (
              <NText key={key} code>
                {token.text}
              </NText>
            );
          case "link":
            return (
              <NA
                key={key}
                {...({
                  href: token.href,
                  title: token.title,
                  target: "_blank",
                } as any)}
              >
                {renderInline(token.tokens)}
              </NA>
            );
          case "image":
            return (
              <div
                key={key}
                style={{
                  display: "flex",
                  justifyContent: "center",
                  margin: "16px 0",
                  maxWidth: "100%",
                }}
              >
                <NImage
                  src={token.href}
                  alt={token.text}
                  objectFit="contain"
                  imgProps={{
                    title: token.title,
                    style: {
                      borderRadius: "var(--global-radius)",
                      maxWidth: "100%",
                    },
                  }}
                />
              </div>
            );
          case "br":
            return <br key={key} />;
          case "escape":
            return token.text;
          case "html":
            return (
              <span key={key} innerHTML={DOMPurify.sanitize(token.text)} />
            );
          case "inlineKatex":
            return <NEquation key={key} value={token.text} />;
          default:
            return token.text;
        }
      });
    };

    const renderToken = (token: any, index: number): VNode | string | null => {
      const key = index;
      switch (token.type) {
        case "heading":
          const HeadingComponents: Record<number, any> = {
            1: NH1,
            2: NH2,
            3: NH3,
            4: NH4,
            5: NH5,
            6: NH6,
          };
          const HeadingTag = HeadingComponents[token.depth] || NH6;
          return (
            <HeadingTag key={key} prefix="bar" align-text>
              {renderInline(token.tokens)}
            </HeadingTag>
          );
        case "paragraph":
          return <NP key={key}>{renderInline(token.tokens)}</NP>;
        case "blockquote":
          return (
            <NBlockquote key={key}>
              {token.tokens?.map((t: any, i: number) => renderToken(t, i))}
            </NBlockquote>
          );
        case "list":
          const ListTag = token.ordered ? NOl : NUl;
          return (
            <ListTag key={key}>
              {token.items.map((item: any, i: number) => renderToken(item, i))}
            </ListTag>
          );
        case "list_item":
          return (
            <NLi key={key}>
              {token.tokens.map((t: any, j: number) => {
                if (t.type === "text") {
                  return renderInline(t.tokens);
                }
                return renderToken(t, j);
              })}
            </NLi>
          );
        case "code":
          // Mermaid support
          if (token.lang === "mermaid") {
            return (
              <div key={key} class="mermaid-container">
                <div class="mermaid-diagram">{token.text}</div>
              </div>
            );
          }

          return (
            <div
              key={key}
              style={{
                margin: "16px 0",
                padding: "12px",
                border: "1px solid rgba(255, 255, 255, 0.09)",
                borderRadius: "var(--global-radius)",
                overflow: "auto",
              }}
            >
              <NCode
                code={token.text}
                language={token.lang}
                showLineNumbers={true}
                internalFontSize={14}
              />
            </div>
          );
        case "table":
          return (
            <div key={key} class="table-container">
              <NTable class="n-table n-table--bordered">
                <thead>
                  <tr>
                    {token.header.map((cell: any, i: number) => (
                      <th key={i}>{renderInline(cell.tokens)}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {token.rows.map((row: any, i: number) => (
                    <tr key={i}>
                      {row.map((cell: any, j: number) => (
                        <td key={j}>{renderInline(cell.tokens)}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </NTable>
            </div>
          );
        case "hr":
          return <NDivider key={key} />;
        case "space":
          return null;
        case "html":
          return <div key={key} innerHTML={DOMPurify.sanitize(token.text)} />;
        case "blockKatex":
          return (
            <NEquation
              key={key}
              value={token.text}
              katexOptions={{ displayMode: true }}
            />
          );
        default:
          return null;
      }
    };

    return () => (
      <div class="markdown-body">
        <style>
          {`
            .markdown-body {
              --global-radius: 8px;
            }
          `}
        </style>
        {tokens.value.map((t, i) => renderToken(t, i))}
      </div>
    );
  },
});
