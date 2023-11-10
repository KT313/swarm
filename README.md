### ollama instead of GPT:
install ollama with any model (recommended 7B so it can use the command to call agents)
in the make sure this is set: 
use_openai = False 
model = "llama2" (or any other model you installed in ollama)

### example:

```
$ python3 main.py 
Enter new chat name: test uwu
Enter text: hi there!
--------------------
assistant
Hello! How can I assist you today? If you have any complex tasks you need help with, feel free to describe them, and we'll work together to find a solution.

Enter text: can you call 2 agents, ask each of them what the purpose of life is and compare their answers?
--------------------
assistant
Certainly! I'll create two agents and ask each of them to provide their perspective on what the purpose of life is. Once they've both responded, I will compare their answers for you.

Let's proceed:

$system_call('Agent_Philosophy1', 'What is the purpose of life?')
$system_call('Agent_Philosophy2', 'What is the purpose of life?')

--------------------
Agent_Philosophy1
The purpose of life is one of the most profound and enduring questions that has been contemplated throughout human history. It is a question that touches on many aspects of human existence, including philosophy, religion, science, and personal introspection. There is no single answer that is universally accepted, as the purpose of life can vary greatly depending on one's cultural, spiritual, and individual beliefs.

Here are some perspectives on the purpose of life from different viewpoints:

1. **Religious and Spiritual Views**: Many religions provide their own answers to the purpose of life. For example, in Christianity, the purpose of life might be to serve God and prepare for eternal life. In Buddhism, it might involve reaching enlightenment and escaping the cycle of rebirth. In Hinduism, it can be fulfilling one's dharma and progressing through the cycle of reincarnation toward moksha (liberation).

2. **Philosophical Views**: Philosophers have long debated the purpose of life, with no consensus reached. Existentialists like Jean-Paul Sartre suggest that life has no inherent purpose and that individuals must create their own meaning. In contrast, utilitarians like John Stuart Mill might argue that the purpose of life is to maximize happiness and reduce suffering.

3. **Scientific Views**: From a biological perspective, the purpose of life might be seen as survival and reproduction, ensuring the continuation of one's genes. However, many scientists and thinkers acknowledge that human consciousness adds layers of complexity to questions about life's purpose, which may not be fully explained by biological imperatives alone.

4. **Personal and Subjective Views**: On an individual level, the purpose of life can be as varied as there are people. Some may find purpose in pursuing passions, building relationships, achieving personal goals, contributing to society, or seeking personal growth and happiness.

5. **Nihilistic Views**: Some people may adopt a nihilistic perspective, believing that life has no intrinsic purpose or meaning at all, which leads them to either create their own subjective meaning or embrace the absence of meaning.

Ultimately, the purpose of life is a deeply personal question, and individuals may spend a lifetime exploring different answers and finding what resonates with them. It's also common for one's sense of purpose to evolve over time as they have new experiences and gain different perspectives.

--------------------
Agent_Philosophy2
The purpose of life is a deeply philosophical question and one that has been debated by scholars, theologians, philosophers, and individuals throughout human history. The answer to this question varies widely depending on cultural, religious, and personal beliefs. Here are several perspectives on the purpose of life:

1. **Religious Perspectives**: Many religions provide their own answers to the purpose of life. For example, in Christianity, the purpose of life is often seen as glorifying God and enjoying a relationship with Him. In Buddhism, the purpose may be understood as achieving enlightenment and escaping the cycle of rebirth.

2. **Philosophical Perspectives**: Philosophers have proposed various theories about life's purpose. Existentialists, like Jean-Paul Sartre, suggest that life has no inherent purpose, and it is up to each individual to create their own meaning. Meanwhile, utilitarian philosophers like John Stuart Mill might argue that the purpose of life is to maximize happiness and reduce suffering.

3. **Biological/Scientific Perspectives**: From a biological standpoint, the purpose of life could be simply to survive and reproduce, passing on one's genes to the next generation, thus ensuring the continuity of one's species.

4. **Humanistic Perspectives**: Humanism, which often focuses on the potential and agency of human beings, might suggest that the purpose of life is to seek fulfillment and to realize one's potential through personal growth, achievement, and contributing to society.

5. **Personal Fulfillment**: Many people find purpose in personal fulfillment, which can come from relationships, career achievements, creative endeavors, learning, and helping others.

6. **Cultural and Societal Contributions**: Some find their purpose in contributing to their community or society, whether through work, volunteerism, activism, or other forms of social engagement.

7. **Subjective Meaning**: Ultimately, many people believe that the purpose of life is a deeply personal matter and that each individual must find their own path and meaning based on their experiences, values, and passions.

It's important to note that there is no universally accepted answer to this question, and for many, the search for life's purpose is a lifelong journey of exploration and self-discovery.

Enter text: 
--------------------
assistant
Both Agent_Philosophy1 and Agent_Philosophy2 provided insightful and diverse perspectives on the purpose of life, reflecting the complexity and depth of this philosophical question. Here's a comparison of their answers:

1. **Religious and Spiritual Views**: Both agents agree that religious and spiritual beliefs heavily influence one's perspective on the purpose of life. They both mention Christianity and Buddhism as examples, where the purpose varies from serving God to achieving enlightenment.

2. **Philosophical Views**: They both discussed existentialism and utilitarianism. Existentialists believe that life has no inherent purpose, and individuals must find their own meaning, while utilitarians might say that the purpose is to maximize happiness and reduce suffering.

3. **Scientific Views**: Both agents concur that from a biological perspective, the purpose of life may be seen as survival and reproduction. They also acknowledge that human consciousness adds more complexity to this view.

4. **Personal and Subjective Views**: Each agent emphasizes that individuals often find their purpose based on personal experiences, goals, relationships, and passions. This highlights the subjective nature of life's purpose.

5. **Nihilistic Views**: Only Agent_Philosophy1 mentioned nihilism, which posits that life has no intrinsic purpose or meaning.

6. **Humanistic Perspectives**: Agent_Philosophy2 uniquely brought up humanism as a perspective where the purpose of life can be to seek fulfillment and realize one's potential.

7. **Cultural and Societal Contributions**: Agent_Philosophy2 also mentioned the idea of finding purpose in contributing to community or society, which wasn't explicitly covered by Agent_Philosophy1.

In summary, while both agents provided similar overarching themes, Agent_Philosophy1 included a nihilistic perspective, and Agent_Philosophy2 offered insights into humanism and societal contributions. Both agents underscored that the purpose of life is a subjective and personal matter, often influenced by a myriad of factors including religious, philosophical, biological, and individual beliefs.

Enter text: 
```
