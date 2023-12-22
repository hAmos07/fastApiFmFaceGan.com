<footer class="w-full bg-white pb-2">
    <div class="relative w-full flex items-center invisible md:visible md:pb-6" x-data="getCarouselData()">
        <button class="absolute left-0 bg-blue-800 hover:bg-blue-700 text-white text-2xl font-bold hover:shadow rounded-full w-16 h-16 ml-12" x-on:click="decrement()">&#8592;</button>
        <template x-for="image in images.slice(currentIndex, currentIndex + 6)" :key="images.indexOf(image)">
            <img class="w-1/6 hover:opacity-75" :src="image">
        </template>
        <button class="absolute right-0 bg-blue-800 hover:bg-blue-700 text-white text-2xl font-bold hover:shadow rounded-full w-16 h-16 mr-12" x-on:click="increment()">&#8594;</button>
    </div>
    <div class="w-full container mx-auto flex flex-col items-center">
        <div class="uppercase pb-6">&copy; <strong>{{ domain }}</strong> {{ year }} </div>
    </div>
</footer>
<script>
    function getCarouselData() {
        return {
            currentIndex: 0,
            images: [
                '/static/img/1.png',
                '/static/img/2.png',
                '/static/img/3.png',
                '/static/img/4.png',
                '/static/img/5.png',
                '/static/img/6.png',
                '/static/img/7.png',
                '/static/img/8.png',
                '/static/img/9.png',
                '/static/img/10.png',
                '/static/img/11.png',
            ],
            increment() {
                this.currentIndex = this.currentIndex === this.images.length - 6 ? 0 : this.currentIndex + 1;
            },
            decrement() {
                this.currentIndex = this.currentIndex === this.images.length - 6 ? 0 : this.currentIndex - 1;
            },
        }
    }
</script>