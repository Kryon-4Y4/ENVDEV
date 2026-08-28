import { useRef, useState } from "react";
import {
  KeyboardAvoidingView, Platform, ScrollView, StyleSheet, Text,
  TextInput, TouchableOpacity, View,
} from "react-native";
import { StatusBar } from "expo-status-bar";

// Mac 的局域网 IP（ipconfig getifaddr en0 查得；换网络环境需同步更新）。
// 手机访问不了 127.0.0.1（那是手机自己），且必须和 Mac 同一 WiFi
const API_BASE = "http://192.168.1.148:8001";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const scrollRef = useRef(null);

  async function send() {
    const message = input.trim();
    if (!message || busy) return;
    setInput("");
    setBusy(true);
    setMessages((msgs) => [...msgs, { role: "user", content: message }]);
    try {
      // 用非流式接口：RN 的 fetch 流式支持不稳定，先打通链路（流式进阶可用 react-native-sse）
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, history: messages.filter((m) => m.content) }),
      });
      if (!res.ok) throw new Error("HTTP " + res.status);
      const data = await res.json();
      if (data.reply) {  // 空回复不存历史（防污染，与其它端一致）
        setMessages((msgs) => [...msgs, { role: "assistant", content: data.reply }]);
      }
    } catch (err) {
      setMessages((msgs) => [...msgs, { role: "assistant", content: "请求失败: " + err.message }]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <KeyboardAvoidingView style={styles.app} behavior={Platform.OS === "ios" ? "padding" : undefined}>
      <StatusBar style="dark" />
      <Text style={styles.header}>ENVDEV ChatBot（手机版）</Text>
      <ScrollView
        style={styles.chat}
        ref={scrollRef}
        onContentSizeChange={() => scrollRef.current?.scrollToEnd()}
      >
        {messages.map((m, i) => (
          <View key={i} style={[styles.bubble, m.role === "user" ? styles.user : styles.assistant]}>
            <Text style={m.role === "user" ? styles.userText : styles.assistantText}>{m.content}</Text>
          </View>
        ))}
      </ScrollView>
      <View style={styles.bar}>
        <TextInput
          style={styles.input}
          value={input}
          onChangeText={setInput}
          placeholder="输入消息…"
          onSubmitEditing={send}
          editable={!busy}
        />
        <TouchableOpacity style={styles.button} onPress={send} disabled={busy}>
          <Text style={styles.buttonText}>{busy ? "…" : "发送"}</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  app: { flex: 1, paddingTop: 60, backgroundColor: "#f5f6f8" },
  header: { textAlign: "center", fontSize: 16, fontWeight: "600", padding: 10 },
  chat: { flex: 1, paddingHorizontal: 12 },
  bubble: { maxWidth: "80%", padding: 10, borderRadius: 12, marginBottom: 8 },
  user: { alignSelf: "flex-end", backgroundColor: "#1a73e8" },
  assistant: { alignSelf: "flex-start", backgroundColor: "#ffffff" },
  userText: { fontSize: 15, color: "#fff" },
  assistantText: { fontSize: 15, color: "#222" },
  bar: { flexDirection: "row", padding: 10, gap: 8 },
  input: { flex: 1, backgroundColor: "#fff", borderRadius: 10, paddingHorizontal: 12, fontSize: 15 },
  button: { backgroundColor: "#1a73e8", borderRadius: 10, paddingHorizontal: 18, justifyContent: "center" },
  buttonText: { color: "#fff", fontSize: 15 },
});
