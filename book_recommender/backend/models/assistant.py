from openai import AsyncOpenAI

class BookAssistant:
    def __init__(self, llm_api_key: str, system_message: str="You are a bookstore assistant assisting customers with finding a book to read that fits their preferences.", model: str="gpt-3.5-turbo"):
        self.llm_client = AsyncOpenAI(api_key=llm_api_key)
        self.messages_list = [{"role": "system", "content": system_message}]
        self.model = model
    
    def _search_results_to_context_(self, search_results: list) -> str:
        hits = []
        for hdx, hit in enumerate(search_results):
            title = hit.payload.get("title", "Unknown title")
            author = hit.payload.get("author", "Unknown author")
            description = hit.payload.get("description", "No description available.")
            genres = hit.payload.get("genres", "Unknown genre")

            # Truncate descriptor for brevity
            if len(description) > 150:
                description = description[:150] + "..."

            # Format hit information
            hitstr = (
                f"Result #{hdx + 1}:\n"
                f"Title: {title}\n"
                f"Author: {author}\n"
                f"Description: {description}\n"
                f"Genres: {genres}\n"
            )
            hits.append(hitstr)

        # Combine all hits into a single string
        context = "\n".join(hits)
        return context

    async def respond(self, user_query: str="", search_results: list=[], stream: bool=False):
        if search_results != []: # if search results aren't empty, append them to the user query
            self.search_results = search_results
            context = self._search_results_to_context_(search_results)
            content = (
                f"User message: {user_query}\n"
                f"Related books in stock:\n---\n"
                f"{context}"
            )
            self.messages_list.append({"role": "user", "content": content})
            
        elif user_query != "": # if search results are empty, use the user query directly
            self.messages_list.append({"role": "user", "content": user_query})

        else: # if there is no user query (e.g. upon first loading the application)
            pass

        # Response
        response = await self.llm_client.chat.completions.create(
            messages = self.messages_list,
            model = self.model,
            stream = stream,
        )

        if not stream:
            output = response.choices[0].message.content
            self.messages_list.append({"role": "assistant", "content": output})
            return output
        else:
            # When you stream the response, you need to append to messages_list externally
            return response