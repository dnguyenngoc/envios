export default RestoreStatus = (sta) => {
    
    if (sta === 'not-start' || sta === undefined) return <></>
    else if (sta === 'pending') return <SpinLoading/>
    else if (sta === 'success') return <img src={Done} alt='' className={classes.siconStatus}></img>
    else return <img src={Fail} alt='' className={classes.siconStatus}></img>
}