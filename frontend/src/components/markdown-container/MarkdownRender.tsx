import { defineComponent, computed, type VNode } from "vue";
import { marked, type Tokens } from "marked";
import DOMPurify from "dompurify";
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

// Custom tokenizer for block math $$...$$
const mathBlock = {
  name: "math",
  level: "block",
  start(src: string) {
    // 修复：严格限制行首，避免代码块内误判
    return src.match(/^\$\$/) ? 0 : undefined;
  },
  tokenizer(src: string, tokens: any) {
    // 修复：增加负向预查 (?!\$) 避免跨块匹配风险，但允许单行 Block
    const match = /^\$\$([\s\S]+?)\$\$(?!\$)/.exec(src);
    if (match) {
      return {
        type: "math",
        raw: match[0],
        text: match[1].trim(),
        displayMode: true,
      };
    }
  },
  renderer(token: any) {
    return token.text;
  },
};

// Custom tokenizer for inline math $...$
const mathInline = {
  name: "inlineMath",
  level: "inline",
  start(src: string) {
    // 修复：跳过转义的 \$ (支持 ES2018 lookbehind)
    const match = src.match(/(?<!\\)\$/);
    return match?.index;
  },
  tokenizer(src: string, tokens: any) {
    // 修复：支持内部转义字符 (如 \$)，排除 $$ 开头
    const match = /^\$(?!\$)((?:\\.|[^$\n])*?)\$/.exec(src);
    if (match) {
      return {
        type: "inlineMath",
        raw: match[0],
        text: match[1].trim(),
        displayMode: false,
      };
    }
  },
  renderer(token: any) {
    return token.text;
  },
};

marked.use({ extensions: [mathBlock, mathInline] as any });

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
    const tokens = computed(() => {
      if (!props.content) return [];
      return marked.lexer(props.content);
    });

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
          case "inlineMath":
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
        case "math":
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
