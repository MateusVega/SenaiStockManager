let abrir = document.getElementById('abrir')
let nav = document.getElementById('nav')
let fecharrr = document.getElementById('fecharrr')
let part1 = document.getElementById('part1')
let part2 = document.getElementById('part2')
abrir.addEventListener('click', () => {
    nav.classList.add('abrir-bt')
    nav.style.display = 'block'
    fecharrr.style.display = 'block'
    abrir.style.display = 'none'
    part1.style.display = 'block'
    part2.style.display = 'block'
})

fecharrr.addEventListener('click', () => {
    nav.classList.remove('abrir-bt')
    nav.style.display = 'none'
    fecharrr.style.display = 'none'
    abrir.style.display = 'block'
    part1.style.display = 'none'
    part2.style.display = 'none'
})