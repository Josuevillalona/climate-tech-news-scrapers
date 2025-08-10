import * as vscode from 'vscode';
import { ClimateDataProvider } from './climateDataProvider';
import { ComponentGenerator } from './componentGenerator';
import { QueryOptimizer } from './queryOptimizer';

const CLIMATE_PARTICIPANT_ID = 'moomoo.climate';

interface IChatResult extends vscode.ChatResult {
    metadata: {
        command: string;
    };
}

export function activate(context: vscode.ExtensionContext) {
    // Initialize providers
    const climateDataProvider = new ClimateDataProvider();
    const componentGenerator = new ComponentGenerator();
    const queryOptimizer = new QueryOptimizer();

    // Create the chat participant
    const handler: vscode.ChatRequestHandler = async (
        request: vscode.ChatRequest,
        context: vscode.ChatContext,
        stream: vscode.ChatResponseStream,
        token: vscode.CancellationToken
    ): Promise<IChatResult> => {
        try {
            // Parse the user's request
            const userMessage = request.prompt;
            const command = request.command;

            stream.progress('Analyzing your climate tech query...');

            // Route to appropriate handler based on command or content
            if (command === 'explain') {
                await handleExplainCommand(userMessage, stream, climateDataProvider);
            } else if (command === 'createComponent') {
                await handleCreateComponent(userMessage, stream, componentGenerator);
            } else if (command === 'optimizeQuery') {
                await handleOptimizeQuery(userMessage, stream, queryOptimizer);
            } else {
                await handleGeneralQuery(userMessage, stream, climateDataProvider, componentGenerator);
            }

            return { metadata: { command: command || 'general' } };
        } catch (error) {
            stream.markdown(`❌ **Error**: ${error instanceof Error ? error.message : 'Unknown error occurred'}`);
            return { metadata: { command: 'error' } };
        }
    };

    // Register the chat participant
    const participant = vscode.chat.createChatParticipant(CLIMATE_PARTICIPANT_ID, handler);
    participant.iconPath = vscode.Uri.joinPath(context.extensionUri, 'icon.png');
    participant.followupProvider = {
        provideFollowups(result: IChatResult, context: vscode.ChatContext, token: vscode.CancellationToken) {
            return [{
                prompt: 'Explain how this relates to climate data visualization',
                label: '🌍 Climate Context',
                command: 'explain'
            }, {
                prompt: 'Create a React component for this',
                label: '⚛️ Generate Component',
                command: 'createComponent'
            }, {
                prompt: 'Optimize the Supabase query',
                label: '🚀 Optimize Query',
                command: 'optimizeQuery'
            }];
        }
    };

    // Register commands
    const explainCommand = vscode.commands.registerCommand('moomoo.climate.explain', () => {
        vscode.commands.executeCommand('workbench.panel.chat.view.copilot.focus', {
            query: '@climate /explain '
        });
    });

    const createComponentCommand = vscode.commands.registerCommand('moomoo.climate.createComponent', () => {
        vscode.commands.executeCommand('workbench.panel.chat.view.copilot.focus', {
            query: '@climate /createComponent '
        });
    });

    const optimizeQueryCommand = vscode.commands.registerCommand('moomoo.climate.optimizeQuery', () => {
        vscode.commands.executeCommand('workbench.panel.chat.view.copilot.focus', {
            query: '@climate /optimizeQuery '
        });
    });

    context.subscriptions.push(
        participant,
        explainCommand,
        createComponentCommand,
        optimizeQueryCommand
    );
}

async function handleExplainCommand(
    userMessage: string,
    stream: vscode.ChatResponseStream,
    climateDataProvider: ClimateDataProvider
) {
    stream.markdown('## 🌍 Climate Tech Explanation\n\n');
    
    const explanation = await climateDataProvider.explainConcept(userMessage);
    stream.markdown(explanation);
    
    stream.markdown('\n\n### 📊 Related Data Sources\n');
    const dataSources = climateDataProvider.getRelevantDataSources(userMessage);
    dataSources.forEach(source => {
        stream.markdown(`- **${source.name}**: ${source.description}\n`);
    });
}

async function handleCreateComponent(
    userMessage: string,
    stream: vscode.ChatResponseStream,
    componentGenerator: ComponentGenerator
) {
    stream.markdown('## ⚛️ Generating Climate Data Component\n\n');
    
    const componentSpec = componentGenerator.parseComponentRequest(userMessage);
    stream.markdown(`Creating a **${componentSpec.type}** component for **${componentSpec.purpose}**\n\n`);
    
    const component = componentGenerator.generateComponent(componentSpec);
    
    stream.markdown('### 📁 Component Code\n\n');
    stream.markdown('```tsx\n' + component.code + '\n```\n\n');
    
    stream.markdown('### 🎨 Styling\n\n');
    stream.markdown('```css\n' + component.styles + '\n```\n\n');
    
    stream.markdown('### 📖 Usage Example\n\n');
    stream.markdown('```tsx\n' + component.usage + '\n```');
}

async function handleOptimizeQuery(
    userMessage: string,
    stream: vscode.ChatResponseStream,
    queryOptimizer: QueryOptimizer
) {
    stream.markdown('## 🚀 Supabase Query Optimization\n\n');
    
    const optimization = queryOptimizer.optimizeQuery(userMessage);
    
    stream.markdown('### 📈 Performance Improvements\n\n');
    stream.markdown(optimization.suggestions);
    
    stream.markdown('\n\n### ⚡ Optimized Query\n\n');
    stream.markdown('```sql\n' + optimization.optimizedQuery + '\n```\n\n');
    
    stream.markdown('### 🔍 Explanation\n\n');
    stream.markdown(optimization.explanation);
}

async function handleGeneralQuery(
    userMessage: string,
    stream: vscode.ChatResponseStream,
    climateDataProvider: ClimateDataProvider,
    componentGenerator: ComponentGenerator
) {
    stream.markdown('## 🤖 MooMoo Climate Assistant\n\n');
    
    // Analyze the query type
    const queryType = analyzeQueryType(userMessage);
    
    switch (queryType) {
        case 'data-visualization':
            stream.markdown('I can help you create data visualizations for climate tech data!\n\n');
            stream.markdown('### 📊 Suggested Chart Types:\n');
            stream.markdown('- **Time Series**: For tracking emissions, temperature, or investment trends\n');
            stream.markdown('- **Geographic Maps**: For regional climate data\n');
            stream.markdown('- **Comparison Charts**: For technology performance metrics\n');
            break;
            
        case 'component-development':
            stream.markdown('I can help you build React components for your climate dashboard!\n\n');
            stream.markdown('### ⚛️ Component Suggestions:\n');
            stream.markdown('- **Data Cards**: For displaying key climate metrics\n');
            stream.markdown('- **Interactive Charts**: Using Chart.js or D3.js\n');
            stream.markdown('- **Filter Controls**: For data exploration\n');
            break;
            
        case 'database-query':
            stream.markdown('I can help optimize your Supabase queries for climate data!\n\n');
            stream.markdown('### 🗄️ Query Optimization Tips:\n');
            stream.markdown('- Use proper indexing for time-series data\n');
            stream.markdown('- Implement pagination for large datasets\n');
            stream.markdown('- Cache frequently accessed climate metrics\n');
            break;
            
        default:
            stream.markdown('I\'m here to help with your climate tech dashboard! I can assist with:\n\n');
            stream.markdown('- 🌍 **Climate data concepts** and explanations\n');
            stream.markdown('- ⚛️ **React component** generation\n');
            stream.markdown('- 🚀 **Supabase query** optimization\n');
            stream.markdown('- 📊 **Data visualization** recommendations\n');
    }
}

function analyzeQueryType(message: string): string {
    const lowerMessage = message.toLowerCase();
    
    if (lowerMessage.includes('chart') || lowerMessage.includes('graph') || lowerMessage.includes('visualization')) {
        return 'data-visualization';
    }
    if (lowerMessage.includes('component') || lowerMessage.includes('react') || lowerMessage.includes('tsx')) {
        return 'component-development';
    }
    if (lowerMessage.includes('query') || lowerMessage.includes('supabase') || lowerMessage.includes('database')) {
        return 'database-query';
    }
    
    return 'general';
}

export function deactivate() {}
