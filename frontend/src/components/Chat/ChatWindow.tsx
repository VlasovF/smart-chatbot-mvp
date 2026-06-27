import React, { useState, useRef, useEffect } from "react";
import { useAuth } from "../../hooks/useAuth";
import { chatAPI, ChatMessage, modelsAPI, OllamaModel } from "../../services/api";

interface Settings {
  temperature: number;
  maxTokens: number;
  systemPrompt: string;
  model: string;
}

export const ChatWindow: React.FC = () => {
  const { logout } = useAuth();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [availableModels, setAvailableModels] = useState<OllamaModel[]>([]);
  const [loadingModels, setLoadingModels] = useState(false);
  const modelsLoaded = useRef(false);

  // Настройки из localStorage
  const [settings, setSettings] = useState<Settings>(() => {
    const saved = localStorage.getItem("chat_settings");
    if (saved) {
      return JSON.parse(saved);
    }
    return {
      temperature: 0.7,
      maxTokens: 200,
      systemPrompt: "Ты полезный ассистент. Отвечай кратко и по делу.",
      model: "phi4-mini:3.8b",
    };
  });

  const toggleSettings = async () => {
    const newShowState = !showSettings;
    setShowSettings(newShowState);

    // Загружаем модели только при открытии и если ещё не загружены
    if (newShowState && !modelsLoaded.current) {
      setLoadingModels(true);
      try {
        const token = localStorage.getItem("access_token");
        if (!token) return;

        const response = await modelsAPI.getModels(token);
        setAvailableModels(response.data.models);
        modelsLoaded.current = true;
      } catch (error) {
        console.error("Failed to load models:", error);
      } finally {
        setLoadingModels(false);
      }
    }
  };

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const controllerRef = useRef<AbortController | null>(null);

  // Автоскролл
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Сохраняем настройки при изменении
  useEffect(() => {
    localStorage.setItem("chat_settings", JSON.stringify(settings));
  }, [settings]);

  const sendMessage = async () => {
    if (!inputText.trim() || isGenerating) return;

    const userMessage: ChatMessage = {
      role: "user",
      content: inputText.trim(),
    };

    // Добавляем сообщение пользователя
    setMessages((prev) => [...prev, userMessage]);
    setInputText("");
    setIsGenerating(true);

    // Создаём AbortController для отмены запроса
    controllerRef.current = new AbortController();

    try {
      const token = localStorage.getItem("access_token");
      if (!token) {
        throw new Error("No token found");
      }

      // Подготавливаем историю (последние 10 сообщений)
      const history = [...messages, userMessage];
      const lastMessages = history.slice(-10);

      // Отправляем запрос
      const generator = chatAPI.streamChatFetch(
        {
          messages: lastMessages,
          temperature: settings.temperature,
          max_tokens: settings.maxTokens,
          system_prompt: settings.systemPrompt,
          model: settings.model,
        },
        token
      );

      // Создаём сообщение бота (пустое, будет заполняться)
      const botMessage: ChatMessage = {
        role: "assistant",
        content: "",
      };
      setMessages((prev) => [...prev, botMessage]);

      // Обрабатываем стрим
      for await (const data of generator) {
        if (data.error) {
          throw new Error(data.error);
        }
        if (data.done) {
          break;
        }
        if (data.token) {
          // Добавляем токен к последнему сообщению
          // console.log('Token:', data.token);
          setMessages((prev) => {
            const newMessages = [...prev];
            const last = newMessages[newMessages.length - 1];
            if (last && last.role === "assistant") {
              // last.content += data.token;
              newMessages[newMessages.length - 1] = {
                ...last,
                content: last.content + data.token,
              };
            }
            return newMessages;
          });
        }
      }
    } catch (error) {
      console.error("Error sending message:", error);
      // Добавляем сообщение об ошибке
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "❌ Извините, произошла ошибка. Пожалуйста, попробуйте снова.",
        },
      ]);
    } finally {
      setIsGenerating(false);
      controllerRef.current = null;
    }
  };

  const clearHistory = () => {
    if (controllerRef.current) {
      controllerRef.current.abort();
    }
    setMessages([]);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const updateSetting = <K extends keyof Settings>(key: K, value: Settings[K]) => {
    setSettings((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h2>🤖 Chat Bot</h2>
        <div className="header-actions">
          <button onClick={toggleSettings}>⚙️ Настройки</button>
          <button onClick={clearHistory}>🗑️ Очистить</button>
          <button onClick={logout}>🚪 Выйти</button>
        </div>
      </div>

      {/* Панель настроек */}
      {showSettings && (
        <div className="settings-panel">
          <div className="setting-group">
            <label>
              Модель:
              <select
                value={settings.model}
                onChange={(e) => updateSetting("model", e.target.value)}
                disabled={loadingModels}
              >
                {loadingModels ? (
                  <option>Загрузка...</option>
                ) : availableModels.length > 0 ? (
                  availableModels.map((model) => (
                    <option key={model.name} value={model.name}>
                      {model.name}
                    </option>
                  ))
                ) : (
                  <option value={settings.model}>{settings.model}</option>
                )}
              </select>
            </label>
          </div>
          <div className="setting-group">
            <label>
              Температура: {settings.temperature.toFixed(1)}
              <input
                type="range"
                min="0.2"
                max="1.2"
                step="0.1"
                value={settings.temperature}
                onChange={(e) => updateSetting("temperature", parseFloat(e.target.value))}
              />
            </label>
          </div>
          <div className="setting-group">
            <label>
              Max токенов: {settings.maxTokens}
              <input
                type="range"
                min="50"
                max="500"
                step="50"
                value={settings.maxTokens}
                onChange={(e) => updateSetting("maxTokens", parseInt(e.target.value))}
              />
            </label>
          </div>
          <div className="setting-group">
            <label>
              Системный промпт:
              <textarea
                value={settings.systemPrompt}
                onChange={(e) => updateSetting("systemPrompt", e.target.value)}
                rows={3}
              />
            </label>
          </div>
        </div>
      )}

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="empty-state">
            <p>Начните диалог с ботом!</p>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div key={index} className={`message ${msg.role === "user" ? "user" : "bot"}`}>
              <div className="message-content">
                <strong>{msg.role === "user" ? "👤 Вы" : "🤖 Бот"}:</strong>
                {msg.content ||
                  (msg.role === "assistant" && isGenerating && (
                    <span className="typing-indicator">...печатает</span>
                  ))}
              </div>
            </div>
          ))
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Введите сообщение..."
          disabled={isGenerating}
        />
        <button onClick={sendMessage} disabled={isGenerating || !inputText.trim()}>
          {isGenerating ? "⏳" : "📤"}
        </button>
      </div>
    </div>
  );
};
