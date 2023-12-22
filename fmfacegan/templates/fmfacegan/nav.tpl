<nav class="w-full py-4 bg-blue-800 shadow">
    <div class="w-full container mx-auto flex flex-wrap items-center justify-between">
        <a href="{{ base_uri }}" class="flex items-center mx-auto">
            <img src="/static/img/logo.svg" class="mr-3 h-6 sm:h-9" alt="FM">
            <span class="self-center text-xl font-semibold whitespace-nowrap text-white">FaceGan</span>
        </a>
    </div>
</nav>
<nav class="w-full py-4 border-t border-b bg-gray-100" x-data="{ open: false }">
    <div class="block sm:hidden">
        <a href="./#" class="block md:hidden text-base font-bold uppercase text-center flex justify-center items-center" @click="open = !open">
            {{ menu }} <i :class="open ? 'fa-chevron-down': 'fa-chevron-up'" class="fas ml-2"></i>
        </a>
    </div>
    <div :class="open ? 'block': 'hidden'" class="w-full flex-grow sm:flex sm:items-center sm:w-auto">
        <div class="w-full container mx-auto flex flex-col sm:flex-row items-center justify-center text-sm font-bold uppercase mt-0 px-6 py-2">
			<a href="{{ url }}#generator" class="hover:bg-gray-400 rounded py-2 px-4 mx-2">FM FaceGan</a>
            <a href="{{ url }}#faq" class="hover:bg-gray-400 rounded py-2 px-4 mx-2">{{ faq }}</a>
            <a href="{{ url }}#demo" class="hover:bg-gray-400 rounded py-2 px-4 mx-2">{{ demo }}</a>
			{{ lang_link | safe }}
			{{ contacts_link | safe }}
        </div>
    </div>
</nav>