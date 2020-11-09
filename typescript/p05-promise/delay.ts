function AsyncDelay(ms: number) {
    return new Promise( resolve => setTimeout(resolve, ms) );
}


export async function delay(ms: number) {
    await AsyncDelay(5000);
}